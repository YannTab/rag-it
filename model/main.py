import feeder

if __name__ == "__main__":
    files = 'stocks_hot_nested.json'
    feeder.feed(files)
    print(f'Successfully processed {files}')