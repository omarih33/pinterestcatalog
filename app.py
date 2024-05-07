import streamlit as st
import pandas as pd

def process_data(file, domain_name):
    df = pd.read_csv(file)

    # Rename columns
    df.rename(columns={'Product ID [Non Editable]': 'item_group_id',
                       'SKU': 'id',
                       'Product URL': 'link',
                       'Title': 'title',
                       'Description': 'description',
                       'Hosted Image URLs': 'image_link',
                       'Price': 'price',
                       'Stock': 'availability'
                      }, inplace=True)

    # Create link column
    df['link'] = domain_name + '/' + df['Product Page'] + '/' + df['link']

    # Fill missing values
    df.fillna(method='ffill', inplace=True)

    # Format price
    df['price'] = df['price'].astype(str) + 'USD'

    # Convert availability to 'in stock' or 'out of stock'
    df['availability'] = df['availability'].apply(lambda x: 'in stock' if x >= 1 else 'out of stock')

    # Extract only one image link per product
    df['image_link'] = df['image_link'].str.split(' ').str[0]

    # Save the processed data to a new CSV file
    processed_file = "processed.csv"
    df.to_csv(processed_file, index=False)
    return processed_file

def main():
    st.title("Make your Squarespace products 'Pinterest Ready'")

    file = st.file_uploader("Upload CSV file")
    domain_name = st.text_input("Enter your domain here (e.g., https://yourdomain.com)")

    if file and domain_name:
        processed_file = process_data(file, domain_name)
        st.download_button("Download your Pinterest Catalog", data=open(processed_file, 'rb'), file_name="processed.csv")

if __name__ == '__main__':
    main()
