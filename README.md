# cmutcp-starter-code
Starter code for 15-441/641 project2 TCP in the Wild

# Environment setup 
1. Open AWS console and go to Cloud9, then choose 'Create environment'.
2. Give a name to your environment, click 'Next'.
3. Keep Environment type as direct access, and instance type as t2.micro. Choose Ubuntu Server 18.04 LTS in the platform option.
4. Create the environment.

# Setup starter code
Once you're in cloud9, use the terminal to execute the following commands -
```
cd /home/ubuntu/environment
git clone https://github.com/computer-networks/cmutcp-starter-code.git
cd cmutcp-starter-code/15-441-project-2/
git checkout aws_cloud9
chmod +x install.sh
sudo ./install.sh
make
```
Now the environment should have all the dependencies needed for CP1. You can run 'make test' to ensure that the unit tests are passing for the 'stop-and-wait' model.

# Give access to your teammate

Unfortunately, accessing your teammate's environment is not as easy as clicking on the Zoom link. But it should still be quite easy.
1. Open AWS console and go to IAM. Under "Access management" choose "Users". 
2. Click Add User, give it a name, and choose "AWS Management Console access". Click "Next".
3. On the permission page, choose "Attach existing policies directly". Type in "cloud9" into the search bar, and choose "AWSCloud9User", "AWSCloud9EnvironmentMember", and "AWSCloud9SSMInstanceProfile". Click "Next"
4. Create the user, send the sign-in link as well as password to your teammate.
5. Go back to the cloud9 environment, click "Share" on the top right corner, and invite the user you just created.
