#!/bin/bash

# Create systemd service and timer files for Naukri automation
# Run this script as root or with sudo

# 1. Create the service file
cat > /etc/systemd/system/naukri-automation.service << 'EOF'
[Unit]
Description=Naukri Automation Docker Container
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
User=root
# Change these paths according to your setup
Environment=RESUME_PATH=/home/your-username/naukri-automation/resume
Environment=NAUKRI_USERNAME=your_username
Environment=NAUKRI_PASSWORD=your_password
Environment=CONTAINER_NAME=naukri-automation

# Remove any existing container with the same name
ExecStartPre=-/usr/bin/docker rm -f ${CONTAINER_NAME}

# Run the container
ExecStart=/usr/bin/docker run --name ${CONTAINER_NAME} \
    -v ${RESUME_PATH}:/app/resume \
    -e NAUKRI_USERNAME=${NAUKRI_USERNAME} \
    -e NAUKRI_PASSWORD=${NAUKRI_PASSWORD} \
    naukri-automation

# Clean up: remove the container after execution
ExecStartPost=/usr/bin/docker rm -f ${CONTAINER_NAME}

# Set timeout for the job (30 minutes)
TimeoutStartSec=1800
TimeoutStopSec=30

# Restart policy
Restart=no

[Install]
WantedBy=multi-user.target
EOF

# 2. Create the timer file
cat > /etc/systemd/system/naukri-automation.timer << 'EOF'
[Unit]
Description=Run Naukri Automation Daily at 9 AM IST
Requires=naukri-automation.service

[Timer]
# Run daily at 9:00 AM IST (UTC+5:30, so 3:30 AM UTC)
OnCalendar=*-*-* 03:30:00
# If system was down, run when it comes back up (within 1 hour)
Persistent=true
# Add some randomization to avoid system load spikes (±10 minutes)
RandomizedDelaySec=600

[Install]
WantedBy=timers.target
EOF

# 3. Create environment configuration file (optional)
cat > /etc/systemd/system/naukri-automation.env << 'EOF'
# Naukri Automation Environment Variables
# Edit these values according to your setup

RESUME_PATH=/home/divine-desktop/naukri-automation/resume
NAUKRI_USERNAME=your_username
NAUKRI_PASSWORD=your_password
CONTAINER_NAME=naukri-automation
EOF

echo "=== Systemd files created successfully ==="
echo ""
echo "Next steps:"
echo "1. Edit the environment variables in /etc/systemd/system/naukri-automation.service"
echo "2. Or edit /etc/systemd/system/naukri-automation.env and update service to use it"
echo "3. Reload systemd daemon: sudo systemctl daemon-reload"
echo "4. Enable the timer: sudo systemctl enable naukri-automation.timer"
echo "5. Start the timer: sudo systemctl start naukri-automation.timer"
echo ""
echo "Useful commands:"
echo "- Check timer status: sudo systemctl status naukri-automation.timer"
echo "- List all timers: sudo systemctl list-timers"
echo "- View logs: sudo journalctl -u naukri-automation.service"
echo "- Test service manually: sudo systemctl start naukri-automation.service"
echo "- Stop timer: sudo systemctl stop naukri-automation.timer"
echo "- Disable timer: sudo systemctl disable naukri-automation.timer"
