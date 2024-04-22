# Detailed Documentation for the Hbooker API Client

## Introduction

The Hbooker API Client is a Python library that provides a comprehensive and user-friendly interface to interact with the Hbooker online reading platform. Hbooker is a popular mobile application and website that offers a vast collection of novels, and other literary works. This client library enables developers to automate various tasks within the Hbooker ecosystem, opening up a world of possibilities for integrating Hbooker content and functionality into your own applications or scripts.

## Key Features

The Hbooker API Client offers the following key features:

1. **Authentication**: Seamlessly handle user authentication, including automatic login, token management, and error handling.
2. **Bookshelf Management**: Retrieve your personal bookshelf, add or remove books, and manage your reading progress.
3. **Chapter Access**: Download and read book chapters, including the ability to access encrypted content.
4. **Book Information**: Retrieve detailed information about books, such as metadata, reviews, and related data.
5. **User Profile**: Access and modify your user profile, read notifications, and manage your account settings.
6. **Search and Browsing**: Perform advanced searches, browse popular titles, and explore book categories.
7. **Error Handling**: Robust error handling, with detailed exception reporting and logging capabilities.
8. **Customization**: Customize various client configurations, such as user agent, timeouts, and retry settings.

## Installation

To install the Hbooker API Client, you can use the following pip command:

```
import HbookerAPI
```

Alternatively, you can clone the project repository from GitHub and install it manually:

```
git clone https://github.com/HbookerAPI/HbookerAPI.git
cd HbookerAPI
python setup.py install
```

## Usage

### Getting Started

To begin using the Hbooker API Client, you need to import the `new_client` function and create a new instance of the `HbookerClient` class:

```python
from h_booker_api import new_client

# Create a new Hbooker client with your account and login token
client = new_client(account='your_account', login_token='your_login_token')
```

If you don't have an account or login token yet, you can use the `auto_sign()` method to automatically sign up and retrieve the necessary credentials:

```python
# Create a new Hbooker client and automatically sign up
client = new_client()
auto_sign_result = client.auto_sign()
account = auto_sign_result['data']['reader_info']['account']
login_token = auto_sign_result['data']['login_token']
```

Once you have the account and login token, you can use them to create a new client instance.

### Bookshelf Management

The Hbooker API Client provides a set of methods to manage your bookshelf, including retrieving your shelves, adding or removing books, and tracking your reading progress.

```python
# Get the list of your bookshelves
shelf_list = client.get_shelf_list()
print(shelf_list)

# Get the book list for a specific shelf
shelf_book_list = client.get_shelf_book_list(shelf_id='your_shelf_id')
print(shelf_book_list)

# Add a book to your bookshelf
client.bookshelf_add_shelf(book_id='your_book_id')

# Remove a book from your bookshelf
client.bookshelf_delete_shelf_book(book_id='your_book_id')

# Set the last read chapter for a book
client.save_record(book_id='your_book_id', chapter_id='your_chapter_id')
```

### Chapter Access

The Hbooker API Client allows you to download and read book chapters, including those with encrypted content.

```python
# Get the list of chapters for a book
division_list = client.get_division_list(book_id='your_book_id')
print(division_list)

# Get the updated chapter list for a book
updated_chapters = client.get_updated_chapter_by_division_new(book_id='your_book_id')
print(updated_chapters)

# Get the content of a specific chapter
chapter_content = client.get_chapter_content(chapter_id='your_chapter_id')
print(chapter_content)

# Buy a specific chapter
buy_chapter_response = client.get_buy_cpt_ifm(chapter_id='your_chapter_id')
print(buy_chapter_response)
```

### Book Information

The Hbooker API Client provides methods to retrieve detailed information about books, including metadata, reviews, and related data.

```python
# Get information about a specific book
book_info = client.get_info_by_id(book_id='your_book_id')
print(book_info)

# Get the list of reviews for a book
review_list = client.get_book_review_list(book_id='your_book_id')
print(review_list)

# Get the list of comments for a specific review
review_comment_list = client.get_review_comment_list(review_id='your_review_id')
print(review_comment_list)

# Get the list of replies for a specific comment
comment_reply_list = client.get_bbs_comment_reply_list(comment_id='your_comment_id')
print(comment_reply_list)
```

### User Profile

The Hbooker API Client allows you to access and modify your user profile, read notifications, and manage your account settings.

```python
# Get your user information
user_info = client.get_user_info()
print(user_info)

# Get your personal prop (item) data
prop_data = client.get_pson_prop_data()
print(prop_data)

# Get your message/notification list
message_list = client.get_msg_list()
print(message_list)

# Modify your user information
client.my_mod_info(nickname='new_nickname', gender='1')
```

### Search and Browsing

The Hbooker API Client provides methods to search for books, browse popular titles, and explore book categories.

```python
# Search for books by keyword
search_results = client.get_search(keyword='your_keyword')
print(search_results)

# Get the list of books by a specific tag
tag_book_list = client.get_book_by_tag(tag_name='your_tag')
print(tag_book_list)

# Get the list of popular/ranking books
rank_list = client.get_rank_list()
print(rank_list)

# Get the list of discounted books
discount_list = client.get_discount_list()
print(discount_list)
```

### Error Handling and Logging

The Hbooker API Client includes robust error handling and logging capabilities to help you debug and troubleshoot any issues that may arise.

```python
# Enable logging
client = new_client(logger=True)

# Make a request and handle any exceptions
try:
    response = client.get_shelf_list()
    print(response)
except Exception as e:
    print(f"Error: {e}")
```

The logging output will be written to a file named `requests_log.txt` and also printed to the console.

### Configuration and Customization

The Hbooker API Client allows you to customize various settings and configurations to suit your needs.

```python
# Set the app version
client.common_params_config.set_app_version('3.0.0')

# Set the device token
client.common_params_config.set_device_token('your_device_token')

# Set the maximum number of retries
client.common_params_config.set_max_retry(20)

# Set the request timeout
client.common_params_config.set_timeout(30)

# Set the web site URL
client.common_params_config.set_web_site('https://your-custom-website.com')
```

## Contributing

Contributions to the Hbooker API Client are welcome and encouraged. If you find any issues, have suggestions for improvements, or would like to add new features, please feel free to submit a pull request or open an issue on the project's GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
