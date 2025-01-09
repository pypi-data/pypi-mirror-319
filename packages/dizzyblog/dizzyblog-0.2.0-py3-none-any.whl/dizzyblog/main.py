import json
import os
import sys

# Function to display the menu
def display_menu():
    print("\nWelcome To DizzyBlog!!")
    print("1. Add Post")
    print("2. View Posts")
    print("3. Update Post")
    print("4. Delete Post")
    print("5. Exit")

# Function to add a post
def add_post():
    while True:
        title = input("Enter post title: ").strip()
        if not title:
            print("Title cannot be empty. Please enter a valid title.")
            continue
        content = input("Enter post content: ").strip()
        if not content:
            print("Content cannot be empty. Please enter valid content.")
            continue
        post = {"title": title, "content": content, "comments": []}
        break
    
    '''
    🤔 Why We Use os module , we can learn direclty handling files ,    
    1 ) To check file existence :=> if we not use this module and directly open any file than python throws an error ...
    2 ) Cross Platform Compatibility :=> For file path In window we use "\" and linux,Mac we use "/"  , So if we work in window and use hardcoding , then there may be problem in mac ....
    3 ) And there is a some extra functionalities given by this module is helpful for us , like 
          a) File / Directory Renaming
          b) File Delete 
          c) Change current working directory 
          d) List of all files in directory     
    '''
    
    if os.path.exists('posts.json'):
        with open('posts.json', 'r') as file:
            try:
                posts = json.load(file) # load function JSON file ko Python object (like dictionary or list) mein read aur convert karta hai.
                if not isinstance(posts, list):  # Ensure that posts is a list (instance is a method to check that the data is in a specific type or not)
                    posts = []
            except json.JSONDecodeError:
                posts = []  # In case of invalid JSON, initialize posts as an empty list
    else:
        posts = []

    posts.append(post)

    with open('posts.json', 'w') as file:
        json.dump(posts, file,indent=4)  # indent => Indentation , dump is same like load but wo just read krta hai or ye save krta hai 
    print("Post added successfully.")



# Function to view posts
def view_posts():
    try:
        with open('posts.json', 'r') as file:
            posts = json.load(file)
            print(posts)
            if posts:
                print("\n--- All Posts ---\n")
                for idx, post in enumerate(posts, 1): # enumerate 
                    print(f"{idx}. {post['title']}")
                post_choice = get_valid_post_choice(posts) 
                selected_post = posts[post_choice - 1] # post_choice - 1 (adjusted for Python’s zero-based indexing)
                print(f"\nTitle: {selected_post['title']}\nContent: {selected_post['content']}\n")
                
                # After viewing, show options to comment or view comments
                while True:
                    print("\n1. Write a Comment")
                    print("2. View Comments")
                    print("3. Edit Comments")
                    print("4. Delete Comment")
                    print("5. Back to Main Menu")
                    comment_choice = input("Choose an option: ")

                    if comment_choice == '1':
                        write_comment(posts, selected_post)  # Pass posts so that we can save the updated post back
                    elif comment_choice == '2':
                        view_comments(selected_post)
                    elif comment_choice == '3':
                        edit_comment(selected_post)
                    elif comment_choice == '4':
                        delete_comment(selected_post)
                    elif comment_choice == '5':
                        break
                    else:
                        print("Invalid option, please try again.")
            else:
                print("No posts available.")
    except FileNotFoundError:
        print("No posts file found. Please add a post first.")

# Function to write a comment on a post
def write_comment(posts, post): # Posts argument means k is file mei ja k selected post pr kam kry ...
    comment = input("Enter your comment: ").strip()
    if comment:
        post['comments'].append(comment)
        with open('posts.json', 'w') as file:
            json.dump(posts, file, indent=4)
        print("Comment added successfully.")
    else:
        print("Comment cannot be empty.")

# Function to view comments on a post
def view_comments(post):
    if post['comments']:
        print("\nComments:")
        for idx, comment in enumerate(post['comments'], 1):
            print(f"{idx}. {comment}")
    else:
        print("No comments yet.")

# Function to edit a comment on a post
def edit_comment(post):
    try:
        with open('posts.json', 'r') as file:
            posts = json.load(file)

        if post['comments']:
            view_comments(post)
            try:
                comment_idx = int(input("\nEnter the number of the comment to edit: "))
                if 1 <= comment_idx <= len(post['comments']):
                    new_comment = input("Enter your new comment: ").strip()
                    if new_comment:
                        post['comments'][comment_idx - 1] = new_comment
                        # Save the updated posts back to the file
                        with open('posts.json', 'w') as file:
                            json.dump(posts, file, indent=4)
                        print("Comment updated successfully.")
                    else:
                        print("Comment cannot be empty.")
                else:
                    print("Invalid comment number.")
            except ValueError:
                print("Invalid input. Please enter a valid comment number.")
        else:
            print("No comments to edit.")
    except FileNotFoundError:
        print("No posts file found.")
    except json.JSONDecodeError:
        print("Error decoding posts data.")

# Function to delete a comment on a post
def delete_comment(post):
    try:
        with open('posts.json', 'r') as file:
            posts = json.load(file)

        if post['comments']:
            view_comments(post)
            try:
                comment_idx = int(input("\nEnter the number of the comment to delete: "))
                if 1 <= comment_idx <= len(post['comments']):
                    post['comments'].pop(comment_idx - 1)
                    # Save the updated posts back to the file
                    with open('posts.json', 'w') as file:
                        json.dump(posts, file, indent=4)
                    print("Comment deleted successfully.")
                else:
                    print("Invalid comment number.")
            except ValueError:
                print("Invalid input. Please enter a valid comment number.")
        else:
            print("No comments to delete.")
    except FileNotFoundError:
        print("No posts file found.")
    except json.JSONDecodeError:
        print("Error decoding posts data.")


# Function to update a post
def update_post():
    try:
        with open('posts.json', 'r') as file:
            posts = json.load(file)

        if not posts:
            print("No posts available.")
            return

        print("\n--- All Posts ---")
        for idx, post in enumerate(posts, 1):
            print(f"{idx}. {post['title']}")
        
        post_choice = get_valid_post_choice(posts)
        selected_post = posts[post_choice - 1]
        print(f"Current content: {selected_post['content']}")
        new_content = input("Enter the new content: ").strip()
        if new_content:
            selected_post['content'] = new_content
            with open('posts.json', 'w') as file:
                json.dump(posts, file, indent=4)
            print("Post updated successfully.")
        else:
            print("Content cannot be empty.")
    except FileNotFoundError:
        print("No posts file found.")

# Function to delete a post
def delete_post():
    try:
        with open('posts.json', 'r') as file:
            posts = json.load(file)

        if not posts:
            print("No posts available.")
            return

        print("\n--- All Posts ---")
        for idx, post in enumerate(posts, 1):
            print(f"{idx}. {post['title']}")
        
        post_choice = get_valid_post_choice(posts)
        del posts[post_choice - 1]

        with open('posts.json', 'w') as file:
            json.dump(posts, file, indent=4)

        print("Post deleted successfully.")
    except FileNotFoundError:
        print("No posts file found.")

# Helper function to get valid post choice (index-based)
def get_valid_post_choice(posts):
    while True:
        try:
            post_choice = int(input("\nChoose a post (Enter number): "))
            if 1 <= post_choice <= len(posts):
                return post_choice
            else:
                print(f"Please choose a valid post number between 1 and {len(posts)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Main function to run the program
def main():
    # Check for command-line arguments
    if len(sys.argv) > 1:
        choice = sys.argv[1]  # Get the user's choice from arguments
        sys.argv = sys.argv[:1]  # Clear the arguments after using them
    else:
        choice = None  # No command-line arguments

    while True:
        if not choice:  # If no command-line argument, show menu
            display_menu()
            choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            add_post()
        elif choice == '2':
            view_posts()
        elif choice == '3':
            update_post()
        elif choice == '4':
            delete_post()
        elif choice == '5':
            print("Exiting DizzyBlog.........")
            print("But Hey !!! 🤗 , if you'd like to view the frontend of my project built with Next.js, please visit the following link: https://dizzyblog.vercel.app/. I'd appreciate it if you could leave a comment there as well. ")
            print("Thank you for using DizzyBlog! Have a great day! 😊")
            break
        else:
            print("Invalid choice, please try again.")

        choice = None  # Reset choice to continue the loop interactively

# Run the main function
if __name__ == "__main__":
    main()