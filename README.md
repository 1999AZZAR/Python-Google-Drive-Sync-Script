# Google Drive Sync (GDS) Script README

## Table of Contents

1. [Introduction](#1-introduction)
2. [Setup](#2-setup)
   - [Prerequisites](#prerequisites)
   - [Configuration](#configuration)
3. [Script Overview](#3-script-overview)
   - [Dependencies](#dependencies)
   - [Database Setup](#database-setup)
   - [Google Drive API](#google-drive-api)
   - [Functions](#functions)
   - [Main Loop](#main-loop)
4. [Usage](#4-usage)
5. [Monitoring and Automation](#5-monitoring-and-automation)
6. [File Log Database](#6-file-log-database)
7. [Error Handling](#7-error-handling)

## 1. Introduction

The Google Drive Sync (GDS) script facilitates seamless synchronization between a designated Google Drive folder and a local directory. It harnesses the power of the Google Drive API to detect changes in the Drive, automatically fetching new files, and efficiently managing local deletions.

## 2. Setup

### Prerequisites

- **Python**: Ensure Python is installed on your machine.
- **Google API Credentials**: Obtain API credentials and an API key.
- **SQLite Database**: Set up an SQLite database for tracking file information.

### Configuration

Edit the `.secret` file to provide the API key, credentials path, folder ID, and download path.

## 3. Script Overview

### Dependencies

- `os`: Operating system interactions.
- `googleapiclient`: Google API client library.
- `time`: Time-related functions.
- `io`: File stream operations.
- `sqlite3`: SQLite database connectivity.
- `datetime`: Timestamp generation.

### Database Setup

The script establishes a connection to an SQLite database (`file_log.db`) to log detailed information about downloaded files. It creates a `file_log` table if it doesn't exist, containing columns for file ID, name, download timestamp, and size.

### Google Drive API

GDS leverages the Google Drive API to interact seamlessly with the specified Drive folder. It performs operations such as listing files, downloading files, and retrieving file information.

### Functions

- `list_files(service, folder_id)`: Lists files in the specified Google Drive folder.
- `download_file(service, file_id, file_name, download_path)`: Downloads a file from Google Drive and logs detailed information in the database.
- `remove_file(file_name, download_path)`: Removes a file from the local directory and the database.

### Main Loop

The script operates within an infinite loop, checking for changes in the Google Drive folder at 15-second intervals. It efficiently downloads new files, removes deleted files, and dynamically updates the file list.

## 4. Usage

- Execute the script to commence the synchronization process.
- Monitor the console for real-time download and deletion notifications.

## 5. Monitoring and Automation

GDS seamlessly integrates into background processes, making it ideal for automated execution. Consider configuring system tools (e.g., cron jobs on Unix-based systems) for scheduled runs.

## 6. File Log Database

The `file_log.db` database maintains an exhaustive record of downloaded files, encompassing their names, download timestamps, and sizes.

## 7. Error Handling

While the script lacks explicit error-handling mechanisms, users are encouraged to enhance this aspect based on their specific use cases and potential issues.
