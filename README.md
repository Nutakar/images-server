# :camera: Images server 
A flask web server to handle images in images/ directory
## :rocket: How to launch 
The only thing you need to launch the app is Docker:
```bash
docker-compose up -d
```
The preceding command build images if they don't exist and starts the containers.
## :bulb: Endpoints 
- *http://{hostname}:{port}/images/{image name}*  
  Output an image by it's name
- *http://{hostname}:{port]/image*  
  List info about all images in the directory with name, size and last modification date
- *http://{hostname}:{port]/image/{image name}*  
  Remove an image from the directory by it's name
- *http://{hostname}:{port]/image* 
  json body: {'name' : '[name]', 'img_base64' : '[img in base64]'} 
  Create a new image by base 64 string
  
