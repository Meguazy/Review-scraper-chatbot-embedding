# Image reference: https://github.com/chroma-core/chroma/releases
FROM ghcr.io/chroma-core/chroma:latest

# Install dependencies, including procps
RUN apt-get update && apt-get install -y procps && apt-get clean

# Set JAVA_HOME (adjust the path if necessary)
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY chroma_configs/ /app/chroma_configs/
COPY src/ /app/src/
COPY entrypoint.sh /app/entrypoint.sh

# Set the working directory
WORKDIR /app/src

# Set PYTHONPATH
ENV PYTHONPATH=/app/src

# Make scripts executable
RUN chmod +x ../entrypoint.sh
RUN chmod +x submit.sh
RUN chmod +x codeKafka/consumer_elastic.py

# Set the entrypoint to a shell script
ENTRYPOINT ["/app/entrypoint.sh"]