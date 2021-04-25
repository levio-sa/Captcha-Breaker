# Captcha-Breaker
A Chrome Extension for breaking Captcha

Currently breaks only Moodle Captcha

However, successfully created backend image processor that are able to predict the Captcha from .pmg image stored in a folder for both the Kerberos and Webmail captchas. Will integrate into the extension later.


## How to use?
- Currently after loading the extension, we need to go on the particular site(Moodle supported as of now) click on the extension, enter username and password and press submit. This will fill in all the values.

- Captcha Recognition - Go to Fourth/captcha breaker/ kerberos or webmail. Do a `pip install -r requirements.txt`
- If you want to create your own datasets,
  - Delete folders data and checkpoint.
  - Create data/captcha and populate with the test images
  - Run `python src/create_train_data.py`
  - This will create a compressed file containing the training and test data
  - Then Run `python src/train.py`
  - After this completes, you have your training model!
  - Then follow the step below
- If you want to use my data
  - Run `python src/predict.py --fname filename` to get predictions(Model is already trained)
 
Currently, the accuracy of kerberos is good(about 95%) but that of webmail is low(primarily because I did not give as much training data).
