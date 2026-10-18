FROM python:3.12-slim
WORKDIR /opt/studentapp
COPY app/ ./app/
RUN python -m compileall -q app && \
    useradd --system --uid 10001 --home-dir /opt/studentapp studentuser && \
    chown -R studentuser:studentuser /opt/studentapp
USER studentuser
EXPOSE 8080
CMD ["python", "-u", "-m", "app.main"]
