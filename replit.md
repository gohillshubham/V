# JioMart Coupon Testing Script

## Overview

This is an automated testing tool for JioMart coupon codes using Selenium WebDriver. The system generates sequential coupon code variations based on a base pattern and tests them by navigating to JioMart URLs with coupon parameters. The tool uses browser automation to systematically test coupon validity and tracks tested codes for analysis.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Components

**Coupon Generation Engine**
- Uses pattern-based incremental generation from a base coupon code
- Implements character-by-character increment logic for alphanumeric strings
- Tracks changeable positions (digits 0-9, lowercase letters a-z)
- Maintains state for sequential generation without duplicates

**Browser Automation Layer**
- Built on Selenium WebDriver with Chrome browser support
- Implements anti-detection measures to appear as regular user traffic
- Performance optimizations including disabled JavaScript and images
- Configurable headless/headed operation modes

**Configuration Management**
- Centralized configuration class with validation
- URL construction utilities for JioMart coupon testing
- Timeout and retry logic parameters
- File path management for logging and output

**Signal Handling System**
- Graceful shutdown on SIGINT/SIGTERM signals
- State preservation during unexpected termination
- Clean browser session cleanup

### Design Patterns

**Factory Pattern**: Browser options configuration with reusable setup methods
**State Pattern**: Coupon generator maintains current position state for incremental generation
**Template Method**: Test execution follows consistent pattern across coupon variations
**Configuration Object**: Centralized settings management with validation

### Error Handling Strategy

- Retry mechanisms for browser operations
- Timeout handling for page loads
- Graceful degradation when coupons are exhausted
- Signal-based cleanup for interrupted operations

## External Dependencies

**Selenium WebDriver**
- Chrome browser automation
- WebDriver management and configuration
- Element interaction and page navigation

**Chrome Browser**
- Requires Chrome installation for WebDriver operations
- ChromeDriver service for browser control

**System Dependencies**
- Signal handling for Unix-like systems
- File system access for logging and output storage
- Network connectivity for JioMart website access

**JioMart Website**
- Target website: relianceretail.com/JioMart/
- Coupon parameter: jiocpn query string
- Dependent on website availability and structure