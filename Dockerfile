FROM python:3.11.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Set AGENT_BACKEND=langgraph at run time to use the LangGraph backend.
ENV AGENT_BACKEND=crewai

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
