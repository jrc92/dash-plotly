# Continuous Delivery of Plotly Flask Application on GCP 

1. Create Project on GCP
![Create Project](img/create_project.png)

2. Activate Cloud Shell 
![Activate](img/CloudShell.png)

3. Activate project using the following command:
```gcloud config set project [PROJECT_ID]```

4. For the specific project, enable APIs for App Engine Admin and Cloud Build (which we'll need for later)
![APISearch](img/APISearch.png)
![APIEnable](img/APIEnable)

5. Create GitHub Repository and initialize a README.md and .gitignore for Python
![GitHubRepo](img/GitHubRepo.png)

6. Next create a SSH key pair by typing the following in Cloud Shell and press 'Enter' key twice
```ssh-keygen -t rsa```

7. Access your SSH key via the following 

7. going to the profile icon on the top right, and click on Settings. Choose SSH and GPG keys
