# CopyMan
The powerful CLI tool to copy, compress and share your files !
Originally designed to help [TesterMan](https://github.com/seblefevre/testerman) users.

# Usage

CopyMan has four main command, **gather**, **serve**, **targz** and **zip**. Let's see how to use it :

## Gather

Gather allow you to *gather* your files in a same folder. You can copy files you select and folders too. You can filtrate files in folders with an ignore setting.


```
$ python3.5 copyman.py gather -d [Destination folder] -s file1.txt -s file2.mp4 -s Folder1/ -i "*.png"
```

## Serve

Serve allow you to share a folder using FTP.

```
$ python3.5 copyman.py serve --directory Folder1/
```

This example serve the content of *Folder1* at *127.0.0.1:2221* by default.

## targz and zip

targz and zip allow you to gather your files in a package.

```
$ python3.5 copyman.py targz -n Files.tar.gz -s file1.txt -s file2.mp4 -s Folder1/
```
Or
```
$ python3.5 copyman.py zip -n Files.zip -s file1.txt -s file2.mp4 -s Folder1/
```
