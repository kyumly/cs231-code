from builtins import range
import numpy as np


def affine_forward(x, w, b):
    """Computes the forward pass for an affine (fully connected) layer.

    The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
    examples, where each example x[i] has shape (d_1, ..., d_k). We will
    reshape each input into a vector of dimension D = d_1 * ... * d_k, and
    then transform it to an output vector of dimension M.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape (N, M)
    - cache: (x, w, b)
    """
    out = None
    ###########################################################################
    # TODO: Copy over your solution from Assignment 1.                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    input_size = x.shape[0]

    data = x.reshape(input_size, -1)
    out = (data @ w) + b

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b)
    return out, cache


def affine_backward(dout, cache):
    """Computes the backward pass for an affine (fully connected) layer.

    Inputs:
    - dout: Upstream derivative, of shape (N, M)
    - cache: Tuple of:
      - x: Input data, of shape (N, d_1, ... d_k)
      - w: Weights, of shape (D, M)
      - b: Biases, of shape (M,)

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
    - dw: Gradient with respect to w, of shape (D, M)
    - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Copy over your solution from Assignment 1.                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    input_size = x.shape[0]
    dw = (x.reshape(input_size, -1).T @ dout)
    dx = (dout @ w.T).reshape(x.shape)
    db = dout.sum(axis=0)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def relu_forward(x):
    """Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    ###########################################################################
    # TODO: Copy over your solution from Assignment 1.                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    out = np.maximum(0, x)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = x
    return out, cache


def relu_backward(dout, cache):
    """Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    ###########################################################################
    # TODO: Copy over your solution from Assignment 1.                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    x[x>0] = 1
    x[ x <= 0 ] = 0

    dx = dout * x


    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def softmax_loss(x, y):
    """Computes the loss and gradient for softmax classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    loss, dx = None, None

    ###########################################################################
    # TODO: Copy over your solution from Assignment 1.                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    x -= np.max(x, axis=1).reshape(-1,1)
    x = np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)

    loss = np.sum(-np.log(x[range(x.shape[0]), y])) / x.shape[0]

    x[range(x.shape[0]), y] -= 1
    dx = x / x.shape[0]

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return loss, dx


def batchnorm_forward(x, gamma, beta, bn_param):
    """Forward pass for batch normalization.

    During training the sample mean and (uncorrected) sample variance are
    computed from minibatch statistics and used to normalize the incoming data.
    During training we also keep an exponentially decaying running mean of the
    mean and variance of each feature, and these averages are used to normalize
    data at test-time.


    교육 중에 표본 평균 및 (보정되지 않은) 표본 분산은 미니 배치 통계에서 계산되어 수신 데이터를 정규화하는 데 사용됩니다.
    또한 훈련 중에 기하급수적으로 감소하는 실행 평균을 유지합니다. 각 피쳐의 평균 및 분산, 이들 평균은 정규화에 사용됩니다.
    테스트 시의 데이터.

    At each timestep we update the running averages for mean and variance using
    an exponential decay based on the momentum parameter:

    각 시간 단계에서 다음을 사용하여 평균 및 분산에 대한 실행 평균을 업데이트합니다
    운동량 매개 변수에 기초한 지수 감소:

    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var

    Note that the batch normalization paper suggests a different test-time
    behavior: they compute sample mean and variance for each feature using a
    large number of training images rather than using a running average. For
    this implementation we have chosen to use running averages instead since
    they do not require an additional estimation step; the torch7
    implementation of batch normalization also uses running averages.

    배치 정규화 용지는 다른 테스트 시간을 제안합니다
    동작: 실행 평균을 사용하는 대신 많은 수의 훈련 영상을 사용하여 각 피쳐에 대한 표본 평균 및 분산을 계산합니다.
    이 구현의 경우 추가 추정 단계가 필요하지 않기 때문에 실행 평균을 대신 사용하기로 선택했습니다. 배치 정규화의 torch7 구현도 실행 평균을 사용합니다.


    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    mode = bn_param["mode"]
    eps = bn_param.get("eps", 1e-5)
    momentum = bn_param.get("momentum", 0.9)

    N, D = x.shape
    running_mean = bn_param.get("running_mean", np.zeros(D, dtype=x.dtype))
    running_var = bn_param.get("running_var", np.zeros(D, dtype=x.dtype))

    out, cache = None, None
    if mode == "train":
        #######################################################################
        # TODO: Implement the training-time forward pass for batch norm.      #
        # Use minibatch statistics to compute the mean and variance, use      #
        # these statistics to normalize the incoming data, and scale and      #
        # shift the normalized data using gamma and beta.                     #
        #                                                                     #
        # 미니 배치 통계량을 사용하여 평균 및 분산을 계산하고,
        # 이 통계량을 사용하여 들어오는 데이터를 정규화하고,
        # 감마 및 베타를 사용하여 정규화된 데이터를 확장 및 이동합니다.
        #
        # You should store the output in the variable out. Any intermediates  #
        # that you need for the backward pass should be stored in the cache   #
        # variable.                                                           #
        #                                                                     #
        # You should also use your computed sample mean and variance together #
        # with the momentum variable to update the running mean and running   #
        # variance, storing your result in the running_mean and running_var   #
        # variables.                                                          #
        #                                                                     #
        # Note that though you should be keeping track of the running         #
        # variance, you should normalize the data based on the standard       #
        # deviation (square root of variance) instead!                        #
        # Referencing the original paper (https://arxiv.org/abs/1502.03167)   #
        # might prove to be helpful.                                          #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        x_mean = np.mean(x, axis=0)
        var = np.var(x, axis=0)

        std = np.sqrt(var + eps)
        x_hat = (x - x_mean) / std
        out = gamma * x_hat + beta

        shape = bn_param.get('shape', (N, D))
        axis = bn_param.get('axis', 0)

        cache = x, x_mean, var, std, gamma, x_hat, shape, axis # save for backprop

        if axis == 0:
            running_mean = momentum * running_mean + (1 - momentum) * x_mean # update overall mean
            running_var = momentum * running_var + (1 - momentum) * var  # update overall variance

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == "test":
        #######################################################################
        # TODO: Implement the test-time forward pass for batch normalization. #
        # Use the running mean and variance to normalize the incoming data,   #
        # then scale and shift the normalized data using gamma and beta.      #
        # Store the result in the out variable.                               #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        x_hat = (x - running_mean) / np.sqrt(running_var + eps)
        out = gamma * x_hat + beta

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    else:
        raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

    # Store the updated running means back into bn_param
    bn_param["running_mean"] = running_mean
    bn_param["running_var"] = running_var

    return out, cache


def batchnorm_backward(dout, cache):
    """Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from batchnorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    # Referencing the original paper (https://arxiv.org/abs/1502.03167)       #
    # might prove to be helpful.                                              #
    ###########################################################################
    x, mu, var, std, gamma, x_hat, shape, axis = cache          # expand cache

    # 기하적인 관점
    #dput_shape = dout.shape
    #db = np.ones((1, dput_shape[0]))
    #dbeta = (db @ dout).reshape(-1)
    #print(dbeta)

    # dout_shape = dout.shape
    # dg = np.ones((1, dout_shape[0]))
    # d_hat = dout * x_hat
    #
    # dgamma = (dg @ d_hat)

    dbeta = dout.sum(axis=0)
    dgamma = (dout * x_hat).sum(axis=0)


    dx_hat = dout * gamma

    dstd = -np.sum(dx_hat * (x-mu), axis=0) / (std**2)

    dvar = 0.5 * dstd / std

    dx_1 = dx_hat / std

    dx_2 = 2 * (x - mu) * dvar / len(dout)

    dx_k1 = dx_1 + dx_2

    dmu = -np.sum(dx_k1, axis=0)  # derivative w.t.r. mu

    dx_k2 = dmu / len(dout)  # partial derivative w.t.r. dx

    dx = dx_k1 + dx_k2

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
    """Alternative backward pass for batch normalization.

    For this implementation you should work out the derivatives for the batch
    normalizaton backward pass on paper and simplify as much as possible. You
    should be able to derive a simple expression for the backward pass.
    See the jupyter notebook for more hints.

    Note: This implementation should expect to receive the same cache variable
    as batchnorm_backward, but might not use all of the values in the cache.

    Inputs / outputs: Same as batchnorm_backward
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    #                                                                         #
    # After computing the gradient with respect to the centered inputs, you   #
    # should be able to compute gradients with respect to the inputs in a     #
    # single statement; our implementation fits on a single 80-character line.#
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    _, _, _, std, gamma, x_hat, shape, axis = cache
    dbeta = dout.reshape(shape, order='F').sum(axis=axis)
    dgamma = (dout * x_hat).reshape(shape, order='F').sum(axis=axis)

    dx_hat = dout * gamma
    N = len(dout)

    dx = dx_hat / std

    dx = dx - (((dx * x_hat).sum(axis=0) * x_hat) / N) - (dx.sum(axis=0) / N)



    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def layernorm_forward(x, gamma, beta, ln_param):
    """Forward pass for layer normalization.

    During both training and test-time, the incoming data is normalized per data-point,
    before being scaled by gamma and beta parameters identical to that of batch normalization.

    Note that in contrast to batch normalization, the behavior during train and test-time for
    layer normalization are identical, and we do not need to keep track of running averages
    of any sort.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - ln_param: Dictionary with the following keys:
        - eps: Constant for numeric stability

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    out, cache = None, None
    eps = ln_param.get("eps", 1e-5)
    ###########################################################################
    # TODO: Implement the training-time forward pass for layer norm.          #
    # Normalize the incoming data, and scale and  shift the normalized data   #
    #  using gamma and beta.                                                  #
    # HINT: this can be done by slightly modifying your training-time         #
    # implementation of  batch normalization, and inserting a line or two of  #
    # well-placed code. In particular, can you think of any matrix            #
    # transformations you could perform, that would enable you to copy over   #
    # the batch norm code and leave it almost unchanged?                      #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    bn_param = {"mode": "train", "axis": 1,
                **ln_param}

    [gamma, beta] = np.atleast_2d(gamma, beta)
    out, cache = batchnorm_forward(x.T, gamma.T, beta.T, bn_param)
    out = out.T

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return out, cache


def layernorm_backward(dout, cache):
    """Backward pass for layer normalization.

    For this implementation, you can heavily rely on the work you've done already
    for batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from layernorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for layer norm.                       #
    #                                                                         #
    # HINT: this can be done by slightly modifying your training-time         #
    # implementation of batch normalization. The hints to the forward pass    #
    # still apply!                                                            #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    dx, dgamma, dbeta = batchnorm_backward_alt(dout.T, cache)  # same as batchnorm backprop
    dx = dx.T  # transpose back dx

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
    """Forward pass for inverted dropout.

    Note that this is different from the vanilla version of dropout.
    Here, p is the probability of keeping a neuron output, as opposed to
    the probability of dropping a neuron output.
    See http://cs231n.github.io/neural-networks-2/#reg for more details.

    Inputs:
    - x: Input data, of any shape
    - dropout_param: A dictionary with the following keys:
      - p: Dropout parameter. We keep each neuron output with probability p.
      - mode: 'test' or 'train'. If the mode is train, then perform dropout;
        if the mode is test, then just return the input.
      - seed: Seed for the random number generator. Passing seed makes this
        function deterministic, which is needed for gradient checking but not
        in real networks.

    Outputs:
    - out: Array of the same shape as x.
    - cache: tuple (dropout_param, mask). In training mode, mask is the dropout
      mask that was used to multiply the input; in test mode, mask is None.
    """
    p, mode = dropout_param["p"], dropout_param["mode"]
    if "seed" in dropout_param:
        np.random.seed(dropout_param["seed"])

    mask = None
    out = None

    if mode == "train":
        #######################################################################
        # TODO: Implement training phase forward pass for inverted dropout.   #
        # Store the dropout mask in the mask variable.                        #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        mask = (np.random.rand(*x.shape) < p) / p
        out = x * mask

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == "test":
        #######################################################################
        # TODO: Implement the test phase forward pass for inverted dropout.   #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        out = x

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                            END OF YOUR CODE                         #
        #######################################################################

    cache = (dropout_param, mask)
    out = out.astype(x.dtype, copy=False)

    return out, cache


def dropout_backward(dout, cache):
    """Backward pass for inverted dropout.

    Inputs:
    - dout: Upstream derivatives, of any shape
    - cache: (dropout_param, mask) from dropout_forward.
    """
    dropout_param, mask = cache
    mode = dropout_param["mode"]

    dx = None
    if mode == "train":
        #######################################################################
        # TODO: Implement training phase backward pass for inverted dropout   #
        #######################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        dx = dout * mask
        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    elif mode == "test":
        dx = dout
    return dx


def get_stride_input_data(train, N, data, stride, C, WW, HH, receptive_field):
    for i in range(N):
        input_data = np.lib.stride_tricks.sliding_window_view(data[i], (C, WW, HH))[:,::stride, ::stride].reshape(-1, receptive_field * C).T
        train[i] = input_data


def conv_forward_naive(x, w, b, conv_param):
    """A naive implementation of the forward pass for a convolutional layer.

    The input consists of N data points, each with C channels, height H and
    width W. We convolve each input with F different filters, where each filter
    spans all C channels and has height HH and width WW.

    Input:
    - x: Input data of shape (N, C, H, W)
    - w: Filter weights of shape (F, C, HH, WW)
    - b: Biases, of shape (F,)
    - conv_param: A dictionary with the following keys:
      - 'stride': The number of pixels between adjacent receptive fields in the
        horizontal and vertical directions.
      - 'pad': The number of pixels that will be used to zero-pad the input.

    During padding, 'pad' zeros should be placed symmetrically (i.e equally on both sides)
    along the height and width axes of the input. Be careful not to modfiy the original
    input x directly.

    Returns a tuple of:
    - out: Output data, of shape (N, F, H', W') where H' and W' are given by
      H' = 1 + (H + 2 * pad - HH) / stride
      W' = 1 + (W + 2 * pad - WW) / stride
    - cache: (x, w, b, conv_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the convolutional forward pass.                         #
    # Hint: you can use the function np.pad for padding.                      #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    N, C, H, W = x.shape
    F, _, HH, WW = w.shape
    padding, stride =  conv_param.get('pad', 0), conv_param.get('stride', 1)

    width_out, height_out = int((H + 2*padding - HH) / stride + 1) ,int((W + 2*padding - WW) / stride + 1)
    receptive_field =  int(HH * WW)
    w_out = w.reshape(int(F), int(C) * receptive_field)
    x_pad = np.pad(x, ((0,), (0,), (padding,), (padding,)), mode='constant', constant_values=0)

    train = np.zeros((N, receptive_field * C, width_out * height_out))

    get_stride_input_data(train, N, x_pad, stride, C, WW, HH, receptive_field)

    out = (w_out @ train).reshape(N, F, width_out, height_out)

    b = np.expand_dims(b, axis=(2, 1))

    x = train
    w = w_out

    out = out + b

    conv_param['filter'] = (HH, WW)
    conv_param['IC'] = C
    conv_param['data_pad'] = x_pad.shape


    #out = out.reshape(int(N), int(F), int(width_out), int(height_out))
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b, conv_param)
    return out, cache


def conv_forward_naive2(x, w, b, conv_param):
    """A naive implementation of the forward pass for a convolutional layer.

    The input consists of N data points, each with C channels, height H and
    width W. We convolve each input with F different filters, where each filter
    spans all C channels and has height HH and width WW.

    Input:
    - x: Input data of shape (N, C, H, W)
    - w: Filter weights of shape (F, C, HH, WW)
    - b: Biases, of shape (F,)
    - conv_param: A dictionary with the following keys:
      - 'stride': The number of pixels between adjacent receptive fields in the
        horizontal and vertical directions.
      - 'pad': The number of pixels that will be used to zero-pad the input.

    During padding, 'pad' zeros should be placed symmetrically (i.e equally on both sides)
    along the height and width axes of the input. Be careful not to modfiy the original
    input x directly.

    Returns a tuple of:
    - out: Output data, of shape (N, F, H', W') where H' and W' are given by
      H' = 1 + (H + 2 * pad - HH) / stride
      W' = 1 + (W + 2 * pad - WW) / stride
    - cache: (x, w, b, conv_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the convolutional forward pass.                         #
    # Hint: you can use the function np.pad for padding.                      #
    ###########################################################################
    pad = conv_param['pad']
    stride = conv_param['stride']
    N, C, H, W = x.shape
    F, C, FH, FW = w.shape

    assert (H - FH + 2 * pad) % stride == 0
    assert (W - FW + 2 * pad) % stride == 0
    outH = int(1 + (H - FH + 2 * pad) / stride)
    outW = int(1 + (W - FW + 2 * pad) / stride)

    # create output tensor after convolution layer
    out = np.zeros((N, F, outH, outW))

    # padding all input data
    x_pad = np.pad(x, ((0,0), (0,0),(pad,pad),(pad,pad)), 'constant')
    H_pad, W_pad = x_pad.shape[2], x_pad.shape[3]

    # create w_row matrix
    w_row = w.reshape(F, C*FH*FW)                            #[F x C*FH*FW]

    # create x_col matrix with values that each neuron is connected to
    x_col = np.zeros((C*FH*FW, outH*outW))                   #[C*FH*FW x H'*W']
    for index in range(N):
        neuron = 0
        for i in range(0, H_pad-FH+1, stride):
            for j in range(0, W_pad-FW+1,stride):
                x_col[:,neuron] = x_pad[index,:,i:i+FH,j:j+FW].reshape(C*FH*FW)
                neuron += 1
        out[index] = (w_row.dot(x_col) + b.reshape(F,1)).reshape(F, outH, outW)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x_pad, w, b, conv_param)
    return out, cache

def get_pooling_input_data(train, datas, C, FH, FW, stride):
    train = np.zeros(shape=train)

    # input_data = np.lib.stride_tricks.sliding_window_view(data[i], (C, WW, HH))[:, ::stride, ::stride].reshape(-1,
    #                                                                                                            receptive_field * C).T
    # train[i] = input_data

    # c = sliding_window_view(data[0], (3, 2, 2))[:, ::2, ::2].reshape(-1, 12).T

    for index in range(len(datas)):
        input_data = np.lib.stride_tricks.sliding_window_view(datas[index], (C, FH, FW))[:, ::stride, ::stride].reshape(-1, (C*FH*FW)).T.reshape(C, (FH*FW), -1)
        train[index] = input_data.max(axis=1).reshape(train.shape[1], train.shape[2], train.shape[3])
    return train


def get_stride_new_data(train,dx, stide, IC, FW, FH, RW, RH):
    """
    다시 펼치는 작업
    """
    # print("값 : ", dx.shape)
    # print("훈련 : ", train.shape)
    # print(FW, FH)
    # print(RW, RH)
    # print(stide)

    train = np.zeros(shape=train)
    SH, SW = train.shape[2], train.shape[3]


    index = 0
    for datas in dx:
        row = 0
        col = 0
        for j in datas.T:
            new_data = j.reshape(IC, FH, FW)
            # print(col, col+FH, row, row+FW)
            if (row + FW) > SW:
                col += stide
                row = 0
            if row > SW and col > SH:
                break
            train[index, :, col: col + FH, row:row + FW] += new_data
            row += stide
        index += 1
    return train
    # print("결과 : ", zero_data[0])

def conv_backward_naive(dout, cache):
    """A naive implementation of the backward pass for a convolutional layer.

    Inputs:
    - dout: Upstream derivatives.
    - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    """
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the convolutional backward pass.                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    x, w, b , conv_param = cache

    padding, stride, receptive_field, IC, data_pad = conv_param.get('pad', 0), conv_param.get('stride', 1), conv_param.get('filter', (1,1)), conv_param.get('IC', 1), conv_param.get('data_pad', 0)

    # print(IC)
    RN, RC, RH, RW = dout.shape

    dloss = dout.reshape(RN, RC, -1)
    x_trans = np.transpose(x, (0, 2, 1))
    dw = (dloss @ x_trans).sum(0)
    dw = dw.reshape(RC, IC, receptive_field[0],receptive_field[1])

    db = dout.sum(axis=(0, 2,3))

    dx = (w.T @ dloss)

    x_pad = get_stride_new_data(data_pad, dx,  stride, IC, receptive_field[0], receptive_field[1], RW, RH)
    train = x_pad

    dx = train[:, :, padding:-padding ,padding:-padding]


    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def conv_backward_naive2(dout, cache):
    """A naive implementation of the backward pass for a convolutional layer.

    Inputs:
    - dout: Upstream derivatives.
    - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    """
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the convolutional backward pass.                        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # Helper function (warning: numpy 1.20+ is required)
    to_fields = np.lib.stride_tricks.sliding_window_view

    x_pad, w, b, conv_param = cache  # extract parameters from cache
    print(x_pad.shape)
    S1 = S2 = conv_param['stride']  # stride:  up = down
    P1 = P2 = P3 = P4 = conv_param['pad']  # padding: up = right = down = left
    F, C, HF, WF = w.shape  # filter dims
    N, _, HO, WO = dout.shape  # output dims

    dout = np.insert(dout, [*range(1, HO)] * (S1 - 1), 0, axis=2)  # "missing" rows
    dout = np.insert(dout, [*range(1, WO)] * (S2 - 1), 0, axis=3)  # "missing" columns
    dout_pad = np.pad(dout, ((0,), (0,), (HF - 1,), (WF - 1,)), 'constant')  # for full convolution

    x_fields = to_fields(x_pad, (N, C, dout.shape[2], dout.shape[3]))  # input local regions w.r.t. dout
    dout_fields = to_fields(dout_pad, (N, F, HF, WF))  # dout local regions w.r.t. filter
    w_rot = np.rot90(w, 2, axes=(2, 3))  # rotated kernel (for convolution)
    db = np.einsum('ijkl->j', dout)  # sum over
    dw = np.einsum('ijkl,mnopiqkl->jqop', dout, x_fields)  # correlate
    dx = np.einsum('ijkl,mnopqikl->qjop', w_rot, dout_fields)[..., P1:-P3, P2:-P4]  # convolve

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db

def max_pool_forward_naive(x, pool_param):
    """A naive implementation of the forward pass for a max-pooling layer.

    Inputs:
    - x: Input data, of shape (N, C, H, W)
    - pool_param: dictionary with the following keys:
      - 'pool_height': The height of each pooling region
      - 'pool_width': The width of each pooling region
      - 'stride': The distance between adjacent pooling regions

    No padding is necessary here, eg you can assume:
      - (H - pool_height) % stride == 0
      - (W - pool_width) % stride == 0

    Returns a tuple of:
    - out: Output data, of shape (N, C, H', W') where H' and W' are given by
      H' = 1 + (H - pool_height) / stride
      W' = 1 + (W - pool_width) / stride
    - cache: (x, pool_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the max-pooling forward pass                            #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    poll_width, pool_height ,stride  = pool_param.get('pool_width', 2), pool_param.get('pool_height', 2), pool_param.get('stride', 2)


    N, C, HI, WI = x.shape

    RH = 1 + (HI - pool_height) // stride
    RW = 1 + (WI - poll_width) // stride


    out_shape = (N, C, RH, RW)

    data = get_pooling_input_data(out_shape, x, C, pool_height, poll_width, stride)

    out = data
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, pool_param)
    return out, cache


def max_pool_backward_naive(dout, cache):
    """A naive implementation of the backward pass for a max-pooling layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: A tuple of (x, pool_param) as in the forward pass.

    Returns:
    - dx: Gradient with respect to x
    """
    dx = None
    ###########################################################################
    # TODO: Implement the max-pooling backward pass                           #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    x, pool_param = cache     # expand cache
    N, C, HO, WO = dout.shape # get shape values
    dx = np.zeros_like(x)     # init derivative

    S1 = S2 = pool_param['stride'] # stride: up = down
    HP = pool_param['pool_height'] # pool height
    WP = pool_param['pool_width']  # pool width

    for i in range(HO):
        for j in range(WO):
            [ns, cs], h, w = np.indices((N, C)), i*S1, j*S2
            f = x[:, :, h:(h+HP), w:(w+WP)].reshape(N, C, -1)
            k, l = np.unravel_index(np.argmax(f, 2), (HP, WP))
            dx[ns, cs, h+k, w+l] += dout[ns, cs, i, j]

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx



def spatial_batchnorm_forward(x, gamma, beta, bn_param):
    """Computes the forward pass for spatial batch normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance. momentum=0 means that
        old information is discarded completely at every time step, while
        momentum=1 means that new information is never incorporated. The
        default of momentum=0.9 should work well in most situations.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None

    ###########################################################################
    # TODO: Implement the forward pass for spatial batch normalization.       #
    #                                                                         #
    # HINT: You can implement spatial batch normalization by calling the      #
    # vanilla version of batch normalization you implemented above.           #
    # Your implementation should be very short; ours is less than five lines. #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    N, C, H, W = x.shape
    x = np.moveaxis(x, 1, -1).reshape(-1, C)
    out, cache = batchnorm_forward(x, gamma, beta, bn_param)
    out = np.moveaxis(out.reshape(N, H, W, C), -1, 1)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return out, cache


def spatial_batchnorm_backward(dout, cache):
    """Computes the backward pass for spatial batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial batch normalization.      #
    #                                                                         #
    # HINT: You can implement spatial batch normalization by calling the      #
    # vanilla version of batch normalization you implemented above.           #
    # Your implementation should be very short; ours is less than five lines. #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    N, C, H, W = dout.shape
    dout = np.moveaxis(dout, 1, -1).reshape(-1, C)
    dx, dgamma, dbeta = batchnorm_backward(dout, cache)
    dx = np.moveaxis(dx.reshape(N, H, W, C), -1, 1)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def spatial_groupnorm_forward(x, gamma, beta, G, gn_param):
    """Computes the forward pass for spatial group normalization.

    In contrast to layer normalization, group normalization splits each entry in the data into G
    contiguous pieces, which it then normalizes independently. Per-feature shifting and scaling
    are then applied to the data, in a manner identical to that of batch normalization and layer
    normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (1, C, 1, 1)
    - beta: Shift parameter, of shape (1, C, 1, 1)
    - G: Integer mumber of groups to split into, should be a divisor of C
    - gn_param: Dictionary with the following keys:
      - eps: Constant for numeric stability

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None
    eps = gn_param.get("eps", 1e-5)
    ###########################################################################
    # TODO: Implement the forward pass for spatial group normalization.       #
    # This will be extremely similar to the layer norm implementation.        #
    # In particular, think about how you could transform the matrix so that   #
    # the bulk of the code is similar to both train-time batch normalization  #
    # and layer normalization!                                                #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    N, C, H, W = x.shape
    ln_param = {"shape": (W, H, C, N), "axis": (0, 1, 3), **gn_param}

    x = x.reshape(N * G, -1)
    gamma = np.tile(gamma, (N, 1, H, W)).reshape(N * G, -1)
    beta = np.tile(beta, (N, 1, H, W)).reshape(N * G, -1)

    out, cache = layernorm_forward(x, gamma, beta, ln_param)
    out = out.reshape(N, C, H, W)
    cache = (G, cache)

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return out, cache


def spatial_groupnorm_backward(dout, cache):
    """Computes the backward pass for spatial group normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (1, C, 1, 1)
    - dbeta: Gradient with respect to shift parameter, of shape (1, C, 1, 1)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial group normalization.      #
    # This will be extremely similar to the layer norm implementation.        #
    ###########################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    G, cache = cache
    N, C, H, W = dout.shape
    dout = dout.reshape(N * G, -1)

    dx, dgamma, dbeta = layernorm_backward(dout, cache)
    dx = dx.reshape(N, C, H, W)
    dbeta = dbeta[None, :, None, None]
    dgamma = dgamma[None, :, None, None]

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dgamma, dbeta
