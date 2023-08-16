FROM ubuntu:latest

# Update apt-get list, install Python, and install other appropriate dependencies
RUN apt-get update
RUN apt-get install -y python3 python3-distutils python3-pip python3-apt cron
RUN pip3 install pyserial PyYAML

# Install timezone dependencies and establish docker container timezone
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata
ENV TZ=America/Phoenix
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy necessary files to local docker container environment
ADD crontab /etc/cron.d/simple-cron
ADD utils.py /utils.py
ADD config.yaml /config.yaml
ADD sdi_12_data_collector.py /sdi_12_data_collector.py
ADD sdi_12_data_collector.sh /sdi_12_data_collector.sh
ADD sdi_12_initialization.py /sdi_12_initialization.py

# Create necessary files and directories inside docker container
RUN touch /var/log/cron.log
RUN mkdir -p /Data
RUN mkdir -p /Data/logs

# Establish correct permissions for files
RUN chmod 0644 /etc/cron.d/simple-cron
RUN chmod +x /sdi_12_data_collector.py
RUN chmod +x /sdi_12_data_collector.sh
RUN chmod +x /utils.py
RUN chmod +x /config.yaml

# Run the command on container startup
CMD cron \
    && sleep 5 \
#    && ./sdi_12_data_collector.sh \
    && bash
