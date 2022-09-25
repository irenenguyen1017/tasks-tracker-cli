# Documentation

## Add command

Add new task with a title as a required argument and optional info.

### Usage

```bash
tasks-tracker add [OPTIONS] TITLE
```

### Arguments

| Argument name | Type | Description                        | Required |
|---------------|------|------------------------------------|----------|
| title         | Text | Provide a brief title for the task | True     |

### Options

| Long          | Short | Type                                      | Description                        |
|---------------|-------|-------------------------------------------|------------------------------------|
| --priority    | -p    | [high\|medium\|low]                       | Set task's priority.               |
| --status      | -s    | [not_started\|in_progress\|on_hold\|done] | Set task's status.                 |
| --description | -d    | TEXT                                      | Set task's description.            |
| --start-date  | -sd   | [%d/%m/%Y]                                | Set the start date. E.g 22/02/2022 |
| --end-date    | -ed   | [%d/%m/%Y]                                | Set the end date. E.g 22/02/2022   |
| --help        |       |                                           | Show this message and exit.        |

## List command

Show all tasks with filter options

### Usage

```bash
tasks-tracker list [OPTIONS]
```

### Options

| Long          | Short | Type                                      | Description                        |
|---------------|-------|-------------------------------------------|------------------------------------|
| --priority    | -p    | [high\|medium\|low]                       | Filter by priority.               |
| --status      | -s    | [not_started\|in_progress\|on_hold\|done] | Filter by status.                 |
| --start-date  | -sd   | [%d/%m/%Y]                                | Filter by the date from the start date. E.g 22/02/2022 |
| --end-date    | -ed   | [%d/%m/%Y]                                | Filter by the date before the end date. E.g 22/02/2022   |
| --help        |       |                                           | Show this message and exit.        |


## Update command

Update an existing task with an ID as a required argument and optional info.

### Usage

```bash
tasks-tracker update [OPTIONS] ID
```

### Arguments

| Argument name | Type | Description                        | Required |
|---------------|------|------------------------------------|----------|
| id         | Text | Task ID | True     |

### Options

| Long          | Short | Type                                      | Description                        |
|---------------|-------|-------------------------------------------|------------------------------------|
| --force    | -f    | Bool                     | Force update task.               |
| --title    | -t    | TEXT                     | Set task's title.               |
| --priority    | -p    | [high\|medium\|low]                       | Set task's priority.               |
| --status      | -s    | [not_started\|in_progress\|on_hold\|done] | Set task's status.                 |
| --description | -d    | TEXT                                      | Set task's description.            |
| --start-date  | -sd   | [%d/%m/%Y]                                | Set the start date. E.g 22/02/2022 |
| --end-date    | -ed   | [%d/%m/%Y]                                | Set the end date. E.g 22/02/2022   |
| --help        |       |                                           | Show this message and exit.        |

## Delete command

Delete an existing task with an ID as a required argument.

### Usage

```bash
tasks-tracker delete ID
```

### Arguments

| Argument name | Type | Description                        | Required |
|---------------|------|------------------------------------|----------|
| id         | Text | Task ID | True     |

### Options

| Long          | Short | Type                                      | Description                        |
|---------------|-------|-------------------------------------------|------------------------------------|
| --force    | -f    | Bool                     | Force delete task.               |

## Delete all command

Delete all tasks.

### Usage

```bash
tasks-tracker delete-all
```

### Options

| Long          | Short | Type                                      | Description                        |
|---------------|-------|-------------------------------------------|------------------------------------|
| --force    | -f    | Bool                     | Force delete all tasks.               |
