**AWS Serverless Text-to-Speech Converter**

This project is a simple, scalable, and cost-effective Text-to-Speech (TTS) converter built entirely on AWS serverless technologies. It provides a web interface where users can enter text, which is then converted into spoken audio and played back in the browser.

**Features**
  - Serverless Architecture: No servers to manage, ensuring high availability and pay-per-use pricing.
  - Scalable: Built with AWS Lambda and API Gateway, which scale automatically with demand.
  - Web Interface: Simple and intuitive HTML/JavaScript frontend for user interaction.
  - Real-time Conversion: Converts text to speech and plays audio directly in the browser.
  - Customizable Voice: Easily change the voice by modifying a single parameter in the Lambda function.

**Architecture**
                                                  
The application follows a classic serverless web application pattern. The workflow is as follows:

  - The user enters text into the frontend application hosted on Amazon S3.
  - The JavaScript frontend sends a POST request with the text to an Amazon API Gateway HTTP endpoint.
  - API Gateway triggers an AWS Lambda function, passing the text payload.
  - The Lambda function invokes the Amazon Polly service to synthesize the text into an MP3 audio stream.
  - Lambda base64 encodes the audio and returns it in a specific JSON format required by API Gateway for binary responses.
  - API Gateway decodes the audio and streams the raw binary data back to the browser.
  - The frontend JavaScript receives the audio as a Blob, creates an object URL, and plays it using the HTML5 <audio> element.

**Technology Stack**

  - Frontend: HTML, CSS, JavaScript (ES6+)
  - Backend: Python 3.9
  - AWS Services:
    - Amazon S3: For hosting the static website (HTML, CSS, JS).
    - AWS Lambda: For running the backend code that processes the request.
    - Amazon API Gateway (HTTP API): To create a public RESTful endpoint for the Lambda function.
    - Amazon Polly: The AI service that performs the text-to-speech conversion.
    - AWS IAM: For securely managing permissions between AWS services.

**Setup and Deployment Guide**

Follow these steps to deploy the application in your own AWS account.
Prerequisites
    An AWS Account.
    Basic knowledge of the AWS Management Console.

**Step 1: Create an S3 Bucket for the Static Website**

  - Navigate to the S3 console.
  - Click Create bucket.
  - Give the bucket a unique name (e.g., my-text-to-speech-app-unique-name).
  - Uncheck "Block all public access" and acknowledge the warning. This is necessary to make the website public.
  - Click Create bucket.
  - Go to the Properties tab of your new bucket, scroll down to Static website hosting, click Edit, and enable it.
  - Set the Index document to index.html.
  - Save changes.
  - Go to the Permissions tab, click Edit under Bucket policy, and paste the following policy. Replace YOUR_BUCKET_NAME with your bucket's name.
  
  Generated json    
 ``` {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "PublicReadGetObject",
              "Effect": "Allow",
              "Principal": "*",
              "Action": "s3:GetObject",
              "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
          }
      ]
 }
```

**Step 2: Create an IAM Role for Lambda**

  - Navigate to the IAM console.
  - Go to Roles and click Create role.
  - For Trusted entity type, select AWS service.
  - For Use case, select Lambda and click Next.
  - On the Add permissions page, search for and add the AWSLambdaBasicExecutionRole policy.
  - Click Next.
  - Give the role a name (e.g., PollyLambdaRole) and click Create role.
  - Find your newly created role, open it, and under the Permissions tab, click Add permissions -> Create inline policy.
  - Select the JSON tab and paste the following policy, which allows the function to use Polly. Click Review policy.

  Generated json
  ```{
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "AllowPolly",
              "Effect": "Allow",
              "Action": "polly:SynthesizeSpeech",
              "Resource": "*"
          }
      ]
  }
  ```
  Give the policy a name (e.g., PollyAccessPolicy) and click Create policy.

**Step 3: Create the Lambda Function**

  - Navigate to the Lambda console.
  - Click Create function.
  - Select Author from scratch.
  - Set the Function name (e.g., textToSpeechFunction).
  - Set the Runtime to Python 3.9 (or a newer Python version).
  - Under Permissions, expand Change default execution role and select Use an existing role.
  - Choose the PollyLambdaRole you created in the previous step.
  - Click Create function.
  - In the Code source editor, replace the default code with the contents of lambda_function.py.
  - Click Deploy to save your changes.

**Step 4: Create the API Gateway**

  - Navigate to the API Gateway console.
  - Click Create API and find the HTTP API card. Click Build.
  - Click Add integration.
  - Select Lambda for the integration type.
  - Choose the region your Lambda is in and select your textToSpeechFunction.
  - Give the API a name (e.g., TextToSpeechAPI).
  - Keep the default route as POST and the resource path as /create (or any name you prefer).
  - Keep the default stage $default and auto-deployment enabled.
  - Click Next, then Create.
  - Once created, you will see an Invoke URL at the top of the dashboard. Copy this URL.

**Step 5: Configure and Deploy the Frontend**

  - Open the index.html file in a text editor.
  - Find the fetch call within the <script> tag.
  - Replace the placeholder URL 'https://abcd.execute-api.ap-south-1.amazonaws.com/create' with the Invoke URL you copied from API Gateway.
  - Save the index.html file.
  - Navigate back to your S3 bucket in the AWS console.
  - Go to the Objects tab and click Upload.
  - Add the modified index.html file and complete the upload.

**Step 6: Test Your Application!**

Navigate to your S3 static website URL. You can find this in the S3 bucket's Properties tab, at the bottom, under Static website hosting. Enter some text and click the button to hear it converted to speech!
File Structure
Generated code
 ```  .
  ├── lambda_function.py   # Python code for the AWS Lambda function
  ├── index.html           # The frontend HTML, CSS, and JavaScript
  └── README.md            # This file
 ```
<img width="614" height="674" alt="image" src="https://github.com/user-attachments/assets/55e36dd6-ec36-4fb8-b71e-72bd06e119e7" />
