![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

## MoodMap + Machine Learning 
Our app is an extension of our web app from project 2, that is, MoodMap aims to create emotional awareness through a comprehensive tracker that categorizes emotions into detailed subcategories, enabling users to monitor trends and foster personal growth on a daily and weekly basis.

However, with this app you can now take a picture and save it to your profile and run a machine learning classification model on it to tell you how you're feeling. 


## Team Members

- Francisco Cunningham - [fctico11](https://github.com/fctico11)
- Ahmad Almesned - [ahmadhcs](https://github.com/ahmadhcs)
- Tanuj Sistla - [tanuj123-cyber](https://github.com/tanuj123-cyber)
- Abhi Vachani - [avachani](https://github.com/avachani)


## To run our project, navigate to root directory and use:
- ```docker-compose up --build --force-recreate``` to build and run. 
- This builds and runs the entire project in three docker containers.
- Then navigate to http://0.0.0.0:8000 to see the front end of the web app running and interact with our app. 
- However, we were having a slight issue in facilitating communication through the web-app and machine-learning-client.
- Therefore, to test our machine-learning-client with a sample angry photo we have provided, open a new terminal window and navigate to machine-learning-client directory and run ```python3 model.py```

## Credit For Machine Learning to Tensorflow:
- [link](https://www.tensorflow.org/tutorials/images/classification)
