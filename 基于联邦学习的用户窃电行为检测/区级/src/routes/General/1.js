
import {Upload, message, Button} from 'antd';
import {UploadOutlined} from '@ant-design/icons';
import React from 'react'
const props = {
    name: 'file',
    action: 'http://127.0.0.1:5000/test',
    headers: {
        authorization: 'authorization-text',
    },
    onChange(info) {
        if (info.file.status !== 'uploading') {
            console.log(info.file, info.fileList);
        }
        if (info.file.status === 'done') {
            message.success(`${info.file.name} file uploaded successfully`);
        } else if (info.file.status === 'error') {
            message.error(`${info.file.name} file upload failed.`);
        }
    },
};

export default () => (
    // eslint-disable-next-line react/react-in-jsx-scope
    <Upload {...props}>
        {/* eslint-disable-next-line react/react-in-jsx-scope,react/react-in-jsx-scope,react/react-in-jsx-scope */}
        <Button icon={<UploadOutlined/>}>Click to Upload</Button>
    </Upload>
);