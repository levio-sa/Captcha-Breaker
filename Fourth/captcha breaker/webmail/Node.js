const captchaPredict = require('src/predict')

captchaPredict(YOUR_IMAGE_PATH_or_URL)
  .then(console.log)
  .catch(console.error)