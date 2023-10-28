import streamlit as st
import pandas as pd

def process_data(file, domain_name):
    df = pd.read_csv(file)

    # Function to fill empty values
    def fill_empty_values(df):
        columns_to_fill = ['Product ID [Non Editable]', 'Product Type [Non Editable]', 'Product Page', 
                           'Product URL', 'Title', 'Description', 'SKU']
        # 'ffill' stands for 'forward fill' and will propagate last valid observation forward.
        df[columns_to_fill] = df[columns_to_fill].fillna(method='ffill')
        return df

    # Call the function you just defined
    df = fill_empty_values(df)
    
    # Rename columns and perform other data processing as in your script
    df.rename(columns={'Product ID [Non Editable]': 'item_group_id',
                  'Variant ID [Non Editable]': 'id',
                  'Product Type [Non Editable]': 'Product Type',
                  'Product Page': 'Product Page',
                  'Product URL': 'link',
                  'Title': 'title',
                  'Description': 'description',
                  'SKU': 'SKU',
                  'Option Name 1': 'variant_names',
                  'Option Value 1': 'variant_value',
                  'Option Name 2': 'Option Name 2',
                  'Option Value 2': 'Option Value 2',
                  'Option Name 3': 'Option Name 3',
                  'Option Value 3': 'Option Value 3',
                  'Option Name 4': 'Option Name 4',
                  'Option Value 4': 'Option Value 4',
                  'Option Name 5': 'Option Name 5',
                  'Option Value 5': 'Option Value 5',
                  'Option Name 6': 'Option Name 6',
                  'Option Value 6': 'Option Value 6',
                  'Price': 'price',
                  'Sale Price': 'Sale Price',
                  'On Sale': 'On Sale',
                  'Stock': 'availability',
                  'Categories': 'Categories',
                  'Tags': 'Tags',
                  'Weight': 'Weight',
                  'Length': 'Length',
                  'Width': 'Width',
                  'Height': 'Height',
                  'Visible': 'Visible',
                  'Hosted Image URLs': 'image_link'
                 }, inplace=True)

    # Fill empty cells in item_group_id with value from nearest cell above it
    df['item_group_id'].fillna(method='ffill', inplace=True)
    
    # Create link column by combining domain_name, Product Page, and link
    df['link'] = domain_name + '/' + df['Product Page'] + '/' + df['link']

    # Fill empty cells in link with value from nearest cell above it
    df['link'].fillna(method='ffill', inplace=True)
    
    # Fill empty cells in title with value from nearest cell above it
    df['title'].fillna(method='ffill', inplace=True)
    
    # Fill empty cells in description with value from nearest cell above it
    df['description'].fillna(method='ffill', inplace=True)
    
    # Change availability values to 'in stock' or 'out of stock'
    df['availability'] = pd.to_numeric(df['availability'], errors='coerce')
    df.loc[df['availability'] >= 1, 'availability'] = 'in stock'
    df.loc[df['availability'] == 0, 'availability'] = 'out of stock'
    df['availability'].fillna(method='ffill', inplace=True)
    
    # Distribute image links
    df['image_link'] = df['image_link'].str.split(' ')
    df = df.explode('image_link')
    df['image_link'].fillna(method='ffill', inplace=True)
    
    # Remove items with missing price values
    df.dropna(subset=['price'], inplace=True)
    
    # Ensure that all prices are formatted correctly
    df['price'] = df['price'].map('{:,.2f}USD'.format)

    # Save the processed data to a new CSV file
    df.to_csv("processed.csv", index=False)
    return "processed.csv"

def main():
    st.title("Make your Squarespace products 'Pinterest Ready'")

    file = st.file_uploader("Upload CSV file")
    domain_name = st.text_input("Enter your domain here (e.g., https://yourdomain.com)")

    if file and domain_name:
        processed_file = process_data(file, domain_name)
        st.download_button("Download your Pinterest Catalog", data=open(processed_file, 'rb'), file_name="processed.csv")

if __name__ == '__main__':
    main()
