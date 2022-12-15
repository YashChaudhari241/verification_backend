var ethUtil = require('ethereumjs-util');
var sigUtil = require('eth-sig-util');
var bodyParser = require('body-parser')
var cors = require('cors')
const express = require('express')
const app = express()
app.use(bodyParser.json());
app.use(cors());

const checkSignature = (req, res) => {
  console.log(req.body)
  const { nonce, signature, publicAddress } = req.body;
  if (!signature || !publicAddress)
    return res
      .status(400)
      .send({ error: 'Request should have signature and publicAddress' });
  const msg ="nonce:"+nonce.toString();
  const msgBufferHex = ethUtil.bufferToHex(Buffer.from(msg, 'utf8'));
  const address = sigUtil.recoverPersonalSignature({
    data: msgBufferHex,
    sig: signature
  });
  if (address.toLowerCase() === publicAddress.toLowerCase()) {
    return res
      .status(200)
      .send({address: address.toLowerCase() })
  } else {
    return res
      .status(401)
      .send({ error: 'Signature verification failed' });
  }
}
app.post('/api/signature', checkSignature)
const port = 3000
app.listen(port, () => {
  console.log(`Signature Check listening on port ${port}`)
})