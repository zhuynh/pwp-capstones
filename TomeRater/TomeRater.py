

class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address

    def __repr__(self):
        return "User {}, email: {}, books read: {}".format(self.name, self.email, len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name

    def read_book(self, book, rating='None'):
        self.books[book] = rating

    def get_average_rating(self):
        if len(self.books) > 0:
            return sum([v for v in self.books.values() if type(v) == int])/len(self.books)
        return 0


class Book():
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    # Removed to prevent duplicate ISBNs
    # def set_isbn(self, isbn):
    #     self.isbn = isbn
    #     print("{}'s ISBN been updated".format(self.title))

    def add_rating(self, rating):
        if type(rating) == int and rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating {} for {}".format(rating, self.title))

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_average_rating(self):
        if len(self.ratings) > 0:
            return sum(self.ratings)/len(self.ratings)
        return 0

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{}, a {} manual on {}".format(self.title, self.level, self.subject)


class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}

    # UNIQUE ISBN'S
    def is_unique_isbn(self, isbn):
        if not isbn in [b.get_isbn() for b in self.books.keys()]:
            return True
        else:
            print("ISBN:{} already exists".format(isbn))
            return False

    def create_book(self, title, isbn):
        if self.is_unique_isbn(isbn):
            b = Book(title, isbn)
            self.books[b] = 0
            return b

    def create_novel(self, title, author, isbn):
        if self.is_unique_isbn(isbn):
            b = Fiction(title, author, isbn)
            self.books[b] = 0
            return b

    def create_non_fiction(self, title, subject, level, isbn):
        if self.is_unique_isbn(isbn):
            b = Non_Fiction(title, subject, level, isbn)
            self.books[b] = 0
            return b

    def add_book_to_user(self, book, email, rating='None'):
        if type(book) == Book or issubclass(type(book), Book):
            if email in self.users:
                self.users[email].read_book(book, rating)
                book.add_rating(rating)
                if book in self.books:
                    self.books[book] += 1
                else:
                    self.books[book] = 1
            else:
                print("No user with email {}".format(email))
        else:
            print("This book does not exist!")

    # invaild user '@ character and either .com , .edu , .org'
    # prevent adding emails that already exist
    def add_user(self, name, email, user_books='None'):
        if email in self.users:
            print("Email: \'{}\' already exists".format(email))
        else:
            domain = email[-4:]
            if '@' in email and (domain == '.com' or domain == '.edu' or domain == '.org'):
                self.users[email] = User(name, email)
                if user_books != 'None':
                    for b in user_books:
                        if type(b) == Book:
                            self.add_book_to_user(b, email)
            else:
                print("{} is an invalid email".format(email))

    def print_catalog(self):
        for k in self.books:
            print(str(k))

    def print_users(self):
        for v in self.users.values():
            print(v)

    def most_read_book(self):
        most_read = ""
        times_read = 0
        for key, value in self.books.items():
            if value > times_read:
                most_read = key
                times_read = value
        return most_read

    def highest_rated_book(self):
        highest_rated_book = ""
        rating = 0
        for key, value in self.books.items():
            if key.get_average_rating() > rating:
                highest_rated_book = key
                rating = key.get_average_rating()
        return highest_rated_book

    def most_positive_user(self):
        most_positive_user = ""
        rating = 0
        for key, value in self.users.items():
            if value.get_average_rating() > rating:
                most_positive_user = key
                rating = value.get_average_rating()
        return most_positive_user
