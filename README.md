# Continuous Delivery of Plotly Flask Application on GCP 

1. Create Project on GCP
![Create Project](img/create_project.png)

2. Activate Cloud Shell 
![Activate](img/CloudShell.png)

3. Activate project using the following command:
```gcloud config set project [PROJECT_ID]```

4. For the specific project, enable APIs for App Engine Admin and Cloud Build (which we'll need for later)
![APISearch](img/APISearch.png)
![APIEnable](img/APIEnable.png)

5. Create GitHub Repository and initialize a README.md and .gitignore for Python
![GitHubRepo](img/GitHubRepo.png)

6. Next create a SSH key pair by typing ```ssh-keygen -t rsa``` in Cloud Shell and press 'Enter' key thrice

7. Access your SSH key via ```cat ~/.ssh/id_rsa.pub``` in Cloud Shell. 

8. On GitHub, click on the Profile icon on the top right, and choose Settings >> SSH and GPG keys. Click on 'New SSH Key', copy and paste the ssh-key from the Shell
![SSH](img/ssh.png)

9. 




