import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Layer
from tensorflow.keras.layers import Input, Dense, Dropout, LeakyReLU, ReLU, Activation, Flatten, Reshape, UpSampling2D, Add, Lambda
from tensorflow.keras.layers import Convolution2D, SeparableConv2D, MaxPooling2D, Concatenate, Add, Multiply
from tensorflow.keras import backend as K
from tensorflow import signal, math
import numpy as np

from .sparsenet_models import *


def compute_data_mask( data ):
    ''' generates sparse data and binary mask (nan == 0) '''
    
    #print(data)
    
    sparse_data = tf.expand_dims(data, axis=-1)
    mask = tf.cast( tf.math.logical_not( tf.math.is_nan(sparse_data)), tf.float32)
    
    sparse_data = tf.math.multiply_no_nan(sparse_data, mask) # NaN * 0 = 0
    
    #print(mask.shape)
    #print(sparse_data.shape)
    
    return tf.concat((sparse_data, mask), axis=3)


def spec_predict( l, phdiff ):
    
    #print(l)
    #print(phdiff)
    
    l_spec = tf.signal.fft2d(tf.complex(l[:,:,:,0], 0.0))
    
    #print("l_spec = ", l_spec)
    #print("phdiff = ", phdiff)
        
    l_spec =  tf.multiply(l_spec, phdiff)
    #print("l_spec*phdiff = ", l_spec)
    
    l_out = tf.math.real(tf.signal.ifft2d(l_spec)) 
    l_out = tf.expand_dims(l_out, axis=-1)
    #print("l_out = ", l_out)
    
    return l_out
    
    
def generate_IDW_kernel( ksize=31, exp=1 ):
    K = np.zeros( (ksize,ksize), dtype=np.float32 )
    XX,YY = np.meshgrid( np.arange(ksize), np.arange(ksize) )
    
    XX -= ksize//2
    YY -= ksize//2
    d = np.power( np.sqrt( XX**2 + YY**2 ), exp )
    d[ ksize//2, ksize//2 ] = 1
    K = 1.0/d
    return K.astype(np.float32)


def generate_kernels(n_kernels=10, sz_kernel=21, exp_vals=None):

    if not exp_vals:
        exp_vals = np.linspace(0.6, 4, n_kernels)

    K = np.empty((sz_kernel,sz_kernel,1,0), dtype=np.float32)

    for i in range(len(exp_vals)):

        k = generate_IDW_kernel( ksize=sz_kernel, exp=exp_vals[i])
        k = np.expand_dims( k, axis=(-1,-2))

        K = np.concatenate([K, k], axis=-1)
        
    return K


def create_model_with_prediction( sparsecnn_weights=None, sparsecnn_trainable=False, sparse_second_stage=True ):
    ''' creates a model with fft prediction using the model_sparsecnn as interpolator
        for sparse data'''
    
    model_sparsecnn = create_sparseconv_256_model()
    
    # if weights are provided
    if sparsecnn_weights is not None:
        model_sparsecnn.load_weights(sparsecnn_weights)
        
    if not sparsecnn_trainable:
        for l in model_sparsecnn.layers:
            l.trainable = False
    
    input_data = Input( shape=(256,256,3) )
    input_ph_diff_matrix = Input( shape=(256,256,4) ) # prev_real, prev_imag, next_real, next_imag
    #print(input_data.shape)
    #print(input_ph_diff_matrix.shape)
    
    IpMp = Lambda( lambda x: compute_data_mask(x), name="IpMp" )( input_data[:,:,:,0] )
    IcMc = Lambda( lambda x: compute_data_mask(x), name="IcMc" )( input_data[:,:,:,1] )
    InMn = Lambda( lambda x: compute_data_mask(x), name="InMn" )( input_data[:,:,:,2] )
    #print(IpMp.shape)
    
    
    Op = model_sparsecnn( IpMp )
    On = model_sparsecnn( InMn )
    
    ph_diff_prev = tf.complex(input_ph_diff_matrix[:,:,:,0], input_ph_diff_matrix[:,:,:,1])
    ph_diff_next = tf.complex(input_ph_diff_matrix[:,:,:,2], input_ph_diff_matrix[:,:,:,3])
    #print(input_ph_diff_matrix[:,:,:,0])
    
    Op_pred = Lambda( lambda x: spec_predict( x[0], x[1]), name="predict_prev" )( [Op, ph_diff_prev] )
    On_pred = Lambda( lambda x: spec_predict( x[0], x[1]), name="predict_next" )( [On, ph_diff_next] )
    
    if sparse_second_stage:
        
        # curr sparse data
        Ic = tf.expand_dims( IcMc[...,0], axis=-1 )
        
        # prev curr and next masks
        Mp = tf.expand_dims( IpMp[...,1], axis=-1 )
        Mc = tf.expand_dims( IcMc[...,1], axis=-1 )        
        Mn = tf.expand_dims( InMn[...,1], axis=-1 )
        
        # weights for the 3 channels according to masks
        W = Concatenate()([Mp,8*Mc,Mn])
        W = W / (tf.reduce_sum( W, axis=-1, keepdims=True) +1E-8 )
        
        # weight the 3 data channels according to masks
        V = Concatenate()([Op_pred, Ic, On_pred])
        M = tf.sign( Mp+Mc+Mn )
        V = tf.reduce_sum( V * W , axis=-1, keepdims=True ) * M
        
        
        k = generate_IDW_kernel( ksize=21, exp=2.8 )
        k = np.expand_dims( k, axis=(-1,-2))
        k = tf.constant(k)
                
        # convolve image and mask with fixed kernels
        I_IDW = tf.nn.conv2d( V, k, strides=1, padding="SAME")
        M_IDW = tf.nn.conv2d( M, k, strides=1, padding="SAME")
        I_IDW = Lambda( lambda x: x[0]/(x[1]+1E-9) )( [I_IDW, M_IDW] )
        
        V = (V - I_IDW)*M
        
        V,M = sparse_conv_block( V, M, (5,5), 32)
        V = Activation('relu')( V )
        
        V,M = sparse_conv_block( V, M, (3,3), 16)
        V = Activation('relu')( V )
        
        V,M = sparse_conv_block( V, M, (3,3), 8)
        V = Activation('relu')( V )
        
        V,M = sparse_conv_block( V, M, (1,1), 1)
        V = Activation('linear')( V )
        
        V += I_IDW
        V *= tf.sign(M_IDW)
                
        model = Model(inputs = [input_data,input_ph_diff_matrix], outputs=V )
        
        
    else:
        Oc = model_sparsecnn( IcMc )
        Oc = Lambda( lambda x: x, name="curr" )( Oc )
        Oc = Concatenate()([Op_pred, Oc, On_pred])

        Oc = Convolution2D( 16, (5,5), padding='same', use_bias=True, activation="sigmoid") ( Oc )
        Oc = Convolution2D( 16, (3,3), padding='same', use_bias=True, activation="sigmoid") ( Oc )
        Oc = Convolution2D( 8, (3,3), padding='same', use_bias=True, activation="sigmoid") ( Oc )
        Oc = Convolution2D( 1, (1,1), padding='same', use_bias=True, activation="linear") ( Oc )

        model = Model(inputs = [input_data,input_ph_diff_matrix], outputs=Oc )
    return model
    
