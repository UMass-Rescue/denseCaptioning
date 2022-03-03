# DenseCap

Note: This is not my code. Currently, it is entirely taken from the authors of the paper:

**[DenseCap: Fully Convolutional Localization Networks for Dense Captioning](http://cs.stanford.edu/people/karpathy/densecap/)**,
<br>
[Justin Johnson](http://cs.stanford.edu/people/jcjohns/)\*,
[Andrej Karpathy](http://cs.stanford.edu/people/karpathy/)\*,
[Li Fei-Fei](http://vision.stanford.edu/feifeili/),
<br>
(\* equal contribution)
<br>
Presented at [CVPR 2016](http://cvpr2016.thecvf.com/) (oral)

The model is a deep convolutional neural network trained in an end-to-end fashion on the [Visual Genome](https://visualgenome.org/) dataset.

The authors provide:

- A [pretrained model](#pretrained-model)
- Code to [run the model on new images](#running-on-new-images), on either CPU or GPU
- Code to run a [live demo with a webcam](#webcam-demos)
- [Evaluation code](#evaluation) for dense captioning
- Instructions for [training the model](#training)

Code source:

```
@inproceedings{densecap,
  title={DenseCap: Fully Convolutional Localization Networks for Dense Captioning},
  author={Johnson, Justin and Karpathy, Andrej and Fei-Fei, Li},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and 
             Pattern Recognition},
  year={2016}
}
```

## Installation

Have conda installed, and run the conda environment: luaEnv.

## Running on new images

To run the model on new images, use the script `run_model.lua`. To run the pretrained model on the provided images,
use the following command:

```bash
th run_model.lua -input_image imgs/[image_name].jpg
```

By default this will run in GPU mode; to run in CPU only mode, simply add the flag `-gpu -1`.

This command will write results into the folder `vis/data`. We have provided a web-based visualizer to view these
results; to use it, change to the `vis` directory and start a local HTTP server:

```bash
cd vis
python -m http.server 8181
```

Then point your web browser to [http://localhost:8181/view_results.html](http://localhost:8181/view_results.html).

If you have an entire directory of images on which you want to run the model, use the `-input_dir` flag instead:

```bash
th run_model.lua -input_dir /path/to/my/image/folder
```

This run the model on all files in the folder `/path/to/my/image/folder/` whose filename does not start with `.`.

<!-- The web-based visualizer is the prefered way to view results, but if you don't want to use it then you can instead
render an image with the detection boxes and captions "baked in"; add the flag `-output_dir` to specify a directory
where output images should be written:

```bash
th run_model.lua -input_dir /path/to/my/image/folder -output_dir /path/to/output/folder/
``` -->

The `run_model.lua` script has several other flags; you can [find details here](doc/FLAGS.md#run_modellua).


<!-- ## Training

To train a new DenseCap model, you will following the following steps:

1. Download the raw images and region descriptions from [the Visual Genome website](https://visualgenome.org/api/v0/api_home.html)
2. Use the script `preprocess.py` to generate a single HDF5 file containing the entire dataset
   [(details here)](doc/FLAGS.md#preprocesspy)
3. Use the script `train.lua` to train the model [(details here)](doc/FLAGS.md#trainlua)
4. Use the script `evaluate_model.lua` to evaluate a trained model on the validation or test data
   [(details here)](doc/FLAGS.md#evaluate_modellua)

For more instructions on training see [INSTALL.md](doc/INSTALL.md) in `doc` folder.


## Evaluation

In the paper we propose a metric for automatically evaluating dense captioning results.
Our metric depends on [METEOR](http://www.cs.cmu.edu/~alavie/METEOR/README.html), and
our evaluation code requires both Java and Python 2.7. The following script will download
and unpack the METEOR jarfile:

```bash
sh scripts/setup_eval.sh
```

The evaluation code is **not required** to simply run a trained model on images; you can
[find more details about the evaluation code here](eval/README.md).


## Webcam demos

If you have a powerful GPU, then the DenseCap model is fast enough to run in real-time. We provide two
demos to allow you to run DenseCap on frames from a webcam.

### Single-machine demo
If you have a single machine with both a webcam and a powerful GPU, then you can
use this demo to run DenseCap in real time at up to 10 frames per second. This demo depends on a few extra
Lua packages:

- [clementfarabet/lua---camera](https://github.com/clementfarabet/lua---camera)
- [torch/qtlua](https://github.com/torch/qtlua)

You can install / update these dependencies by running the following:

```bash
luarocks install camera
luarocks install qtlua
```

You can start the demo by running the following:

```bash
qlua webcam/single_machine_demo.lua
```

### Client / server demo
If you have a machine with a powerful GPU and another machine with a webcam, then
this demo allows you use the GPU machine as a server and the webcam machine as a client; frames will be
streamed from the client to to the server, the model will run on the server, and predictions will be shipped
back to the client for viewing. This allows you to run DenseCap on a laptop, but with network and filesystem
overhead you will typically only achieve 1 to 2 frames per second.

The server is written in Flask; on the server machine run the following to install dependencies:

```bash
cd webcam
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
cd ..
```

For technical reasons, the server needs to serve content over SSL; it expects to find SSL key
files and certificate files in `webcam/ssl/server.key` and `webcam/ssl/server.crt` respectively.
You can generate a self-signed SSL certificate by running the following:

```bash
mkdir webcam/ssl

# Step 1: Generate a private key
openssl genrsa -des3 -out webcam/ssl/server.key 1024
# Enter a password

# Step 2: Generate a certificate signing request
openssl req -new -key webcam/ssl/server.key -out webcam/ssl/server.csr
# Enter the password from above and leave all other fields blank

# Step 3: Strip the password from the keyfile
cp webcam/ssl/server.key webcam/ssl/server.key.org
openssl rsa -in webcam/ssl/server.key.org -out webcam/ssl/server.key

# Step 4: Generate self-signed certificate
openssl x509 -req -days 365 -in webcam/ssl/server.csr -signkey webcam/ssl/server.key -out webcam/ssl/server.crt
# Enter the password from above
```

You can now run the following two commands to start the server; both will run forever:

```bash
th webcam/daemon.lua
python webcam/server.py
```

On the client, point a web browser at the following page:

```
https://cs.stanford.edu/people/jcjohns/densecap/demo/web-client.html?server_url=SERVER_URL
```

but you should replace SERVER_URL with the actual URL of the server.

**Note**: If the server is using a self-signed SSL certificate, you may need to manually
tell your browser that the certificate is safe by pointing your client's web browser directly
at the server URL; you will get a message that the site is unsafe; for example on Chrome
you will see the following:

<img src='imgs/chrome_ssl_screen.png'>

Afterward you should see a message telling you that the DenseCap server is running, and
the web client should work after refreshing. -->

