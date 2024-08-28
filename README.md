# Multi-User Payment Service

This repository contains the submission for the Web Applications and Services module assignment. The project involves the design and implementation of a simplified web-based, multi-user payment service using the Django framework. The system functions similarly to PayPal, allowing users to send and receive money, request payments, and manage their accounts, with administrative access for super-users to oversee all transactions.

## Assignment Overview

### Project Description

The goal of this project is to create a Django-based web application where users can:
- Register with a username, first and last name, email address, password, and choose their account currency (GBP, USD, or EUR).
- Manage their accounts, including viewing their current balance and transaction history.
- Send money to other registered users, with real-time notifications.
- Request money from other users and handle incoming payment requests.
- Super-users (administrators) have access to view all user accounts and transactions.

### Features

1. **User Registration and Account Management**:
   - Users register with personal details and select a currency.
   - Initial account balance set based on currency choice with hard-coded conversion rates.

2. **Payment Transactions**:
   - Users can send payments to others, provided the recipient exists and there are sufficient funds.
   - Transactions are handled securely using Django transactions to ensure atomicity.

3. **Payment Requests**:
   - Users can request payments from others, with options for recipients to accept or reject requests.
   - Notifications are sent for incoming payments and requests.

4. **Transaction History**:
   - Users can view a complete history of their sent, received, and requested transactions.
   - Super-users can view all transactions across all users.

5. **Currency Conversion Service**:
   - A separate RESTful web service handles currency conversion between currencies using hard-coded exchange rates.


## Repository Structure

- `payapp/`: The Django application handling the payment services including sending and receiving money

- `register/`: The Django application handling the all services about user management

- `conversion/`: The Django application for the currency conversion API

- `templates/`: Contains HTML templates for the user interface.

- `thrift_service/`: Contains the implementation of the Thrift timestamp service.

- `requirements.txt`: Lists the required Python libraries and dependencies for running the project.
