var ALY = require('aliyun-sdk'),
  fs = require('fs');

var ossStream = require('aliyun-oss-upload-stream')(new ALY.OSS({
  accessKeyId: process.env.OSS_ACCESS_KEY_ID,
  secretAccessKey: process.env.OSS_ACCESS_KEY_SECRET,
  endpoint: 'http://oss-cn-beijing.aliyuncs.com',
  apiVersion: '2013-10-15'
}));

var upload = ossStream.upload({
  Bucket: 'oneflow-static',
  Key: process.env.OSS_OBJECT_KEY
});

// 可选配置
upload.minPartSize(1048576); // 1M，表示每块part大小至少大于1M

upload.on('error', function (error) {
  console.log('error:', error);
});

upload.on('part', function (part) {
  console.log('part:', part);
});

upload.on('uploaded', function (details) {
  var s = (new Date() - startTime) / 1000;
  console.log('details:', details);
  console.log('Completed upload in %d seconds', s);
});

var read = process.stdin;
read.pipe(upload);

var startTime = new Date();
