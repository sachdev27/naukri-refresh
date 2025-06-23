# Use selenium/standalone-chrome as the base image (comes with Chrome and Selenium preinstalled)
FROM selenium/standalone-chrome:latest

# Set working directory
WORKDIR /app

# Copy the Python script and requirements
COPY naukri.py .
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a volume for the resume
VOLUME /app/resume

# Set environment variables for the script (to be overridden at runtime)
ENV NAUKRI_USERNAME=""
ENV NAUKRI_PASSWORD=""
ENV ORIGINAL_RESUME_PATH="/app/resume/Resume.pdf"
ENV NAUKRI_LOGIN_URL="https://www.naukri.com/nlogin/login"
ENV NAUKRI_PROFILE_URL="https://www.naukri.com/mnjuser/profile"

# Keep container running for manual execution
CMD ["tail", "-f", "/dev/null"]


## Working Commands
# docker run -it -v $(pwd)/resume:/app/resume naukri-automation
# docker run -it -v $(pwd)/resume:/app/resume -e NAUKRI_USERNAME="your_username" -e NAUKRI_PASSWORD="your_password" naukri-automation