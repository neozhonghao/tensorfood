<center><h1>Tensorfood 😋</h1></center>

## 0. About

<b>Tensorfood</b> is the most amazing Singapore food classifier ever. It is able to identify more than 10 different kinds of Singaporean dishes. Whether it is the world renowned Chilli Crab or the smooth and silky tau huay, Tensorfood can identify them all. What you have to do is simply to upload a picture of the food and Tensorfood will tell you the name. It is that simple.

To celebrate the launch of tensorfood, we have added 🌟🌟🌟<b>NEW BONUS FEATURE</b>🌟🌟🌟  in Tensorfood. Tensorfood will not only tell you the name of the food but also the confidence that the food is right. Worth it!

With Tensorfood, remember, no more 我要这个，我要那个 when ordering your meals from the caipeng uncle.

*Not applicable to Malaysian food.

## 1. Installation & Deployment

<b>Tensorfood</b> can be deployed on any machine that has [docker](https://www.docker.com/) installed. For instructions on installing docker on your specific machine, please visit [install docker packages](https://hub.docker.com/search?q=&type=edition&offering=community).

#### Cloning onto Machine
To install the current release, you will need to set up Git (if you haven't done so) and then clone (copy) the repository.

Set up an ssh config file with the following information
```
Host gitlab.int.aisingapore.org
HostName gitlab.int.aisingapore.org
User git
Port 2022
IdentityFile ~/.ssh/id_ed25519
IdentitiesOnly Yes
```

And then clone my branch onto your machine. You may use either of the two commands.
```
$ git clone -b deploy-zhong_hao_neo git@gitlab.int.aisingapore.org:aiap/aiap6/all-assignments.git
```

Or

```
$ git clone -b deploy-zhong_hao_neo https://gitlab.int.aisingapore.org/aiap/aiap6/all-assignments.git
```

#### Building and deploying the API
To run the app, you will be setting up a model as a RESTful api microservice. During deployment, the user will request a query (food image) to the api and then the model will respond with the name of the food.


First we enter into the app directory (work directory).
```
$ cd all-assignments/assignments/assignment7
```

The api will be deployed as a docker container. This is to provide a consistent environment for the app to run. Here, we will build the docker image.
```
$ docker build -tag tensorfood:1.0 .
```

Run the image as a container. Users will make the queries on port 8000.
```
$ docker run --publish 8000:8000 --name tensorfood_app tensorfood:1.0
```

## 2. Software
After the app is being deployed, the image query can be made using any browser or curl!

For those using browsers, head over to your favorite browsers and enter hosting website using the previous port number.
```
localhost:8000
```

For those using curl, fire up your favorite terminal and use the following command.
```
curl -F "image=@C:\Users\neozhonghao\Desktop\AIAP\Assignments\assignment7\data\image_ice_kacang.jpg"
```


## 3. Model

#### Architecture
The model architecture is quite straightforward since it uses transfer learning. The trained base model is Xception, which is a model developed by Google. Xception has 20861480 parameters, but because it is the base model, these parameters will be frozen. Following the base model, a pooling layer to consolidate the output dimensions and a fully connected dense layer of 12 units is connected to the model. The 12 units correspond to the probability of the 12 food classes. The full model architecture is as shown below.

```
Model: "transfer"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
input (InputLayer)           [(None, 200, 300, 3)]     0         
_________________________________________________________________
tf_op_layer_RealDiv (TensorF [(None, 200, 300, 3)]     0         
_________________________________________________________________
tf_op_layer_Sub (TensorFlowO [(None, 200, 300, 3)]     0         
_________________________________________________________________
xception (Functional)        (None, 7, 10, 2048)       20861480  
_________________________________________________________________
pool (GlobalAveragePooling2D (None, 2048)              0         
_________________________________________________________________
dropout_out (Dropout)        (None, 2048)              0         
_________________________________________________________________
output (Dense)               (None, 12)                24588     
=================================================================
Total params: 20,886,068
Trainable params: 24,588
Non-trainable params: 20,861,480
_________________________________________________________________
None
```

#### Training
The model trained was trained with a learning rate of 0.001 using the adam optimizer. The loss function is the cross entropy. An early stopping of patience 3 with a minimum delta of 2 was employed to prevent overfitting. No regularization was used, although for subsequent iterations, regularizations can be applied as there were some indications of overfitting.

#### Testing
The model managed to achieve an average of 0.893 accuracy for the test set. The average F1 score is 0.929 across all 12 classes.

| No. | Food | Precision | Recall |  F1  |
| :-- | :--: | :-------: | :----: | :--: |
| 1 | chilli_crab | 0.8636363636363636 | 0.95 | 0.9047619047619048 |
| 2 | curry_puff | 1.0 | 1.0 | 1.0 |
| 3 | dim_sum | 0.9523809523809523 | 1.0 | 0.975609756097561 |
| 4 | ice_kacang | 1.0 | 1.0 | 1.0 |
| 5 | kaya_toast | 0.8333333333333334 | 1.0 | 0.9090909090909091 |
| 6 | nasi_ayam | 0.8421052631578947 | 0.8 | 0.8205128205128205 |
| 7 | popiah | 1.0 |0.9 | 0.9473684210526315 |
| 8 | roti_prata | 1.0 | 0.9 | 0.9473684210526315 |
| 9 | sambal_stingray | 0.95 | 0.95 | 0.95 |
| 10 | satay | 0.8421052631578947 | 0.8 | 0.8205128205128205 |
| 11 | tau_huay | 1.0 | 0.95 | 0.9743589743589743 |
| 12 | wanton_noodle | 0.9 | 0.9 | 0.9 |


## 4. CI/CD Pipeline

#### Continuous Integration
Continuous Integration is the practice of integrating code into a shared repository and building/testing each change automatically, as early as possible – usually several times a day.

#### Continuous Development
Continuous Delivery ensures CI-validated code can be released to production at any time.

CI/CD automates workflows and reduces error rates within a production environment, which can have far-reaching impacts on not just development teams but throughout a whole organization.

- More time for innovation
- Better retention rates
- More revenue
- Business efficiency

For example, a dev environment with less manual tasks means that engineers can spend more time on revenue-generating projects. With fewer errors, teams are more efficient and spend less time putting out fires. When processes, such as unit testing, are automated, engineers are happier and can focus on where they add the most value.

CI/CD brings automation into the DevOps lifecycle. With less manual work, DevOps teams work more efficiently and with greater speed. An automated workflow also reduces the chance of human error and improves handoffs, which improves overall operational efficiency. Organizations that implement CI/CD make better use of their resources and will have a competitive edge over those that don't use CI/CD.
