# Task Manager

A simple command-line task management application built with Python that helps you track time spent on different tasks.

## Features

- Start and stop task timing
- View task history and statistics
- Track multiple sessions per task
- View detailed session information
- Delete tasks
- Persistent storage using JSON

## Requirements

- Python 3.11 or higher
- Poetry for dependency management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shahinabdi/maktabkhooneh.git
cd maktabkhooneh/CH03/taskmanager
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Project Structure

```
taskmanager/
├── src/
│   └── taskmanager/
│       ├── controllers/
│       │   └── task_controller.py
│       ├── models/
│       │   └── task_model.py
│       ├── views/
│       │   └── task_view.py
│       └── main.py
├── tests/
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Usage

1. Start the application:
```bash
poetry run python src/taskmanager/main.py
```

2. Use the menu options to:
   - Start a new task
   - Stop the current task
   - View task details and sessions
   - Delete tasks
   - Exit the application

### Menu Options

1. **Start Task**: Begin timing a new task
   - Enter the task name
   - Cannot start a new task while another is running

2. **Stop Task**: Stop the current running task
   - Shows duration of the completed session
   - Saves session information

3. **View Task**: Browse and view task details
   - See list of all tasks
   - View basic information
   - View all sessions
   - View last 3 sessions

4. **Delete Task**: Remove a task and its history
   - Select from list of existing tasks
   - Permanent deletion

5. **Exit**: Close the application
   - Cannot exit while a task is running

## Data Storage

Tasks and sessions are stored in a JSON file (`tasks.json`) with the following structure:

```json
{
    "task_name": {
        "total_time": 0.0,
        "sessions": [
            {
                "start": "YYYY-MM-DD HH:MM:SS",
                "end": "YYYY-MM-DD HH:MM:SS",
                "duration": 0.0
            }
        ]
    }
}
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Coverage

```bash
poetry run pytest --cov=src/taskmanager
```

## Architecture

The application follows the Model-View-Controller (MVC) pattern:

- **Model** (`TaskModel`): Handles data management and business logic
- **View** (`TaskView`): Manages user interface and input/output
- **Controller** (`TaskController`): Coordinates between Model and View

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
MIT

## Author

Shahin ABDI - contact@shahinabdi.fr
