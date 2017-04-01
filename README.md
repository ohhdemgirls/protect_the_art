# Mr. Fourchan

Scripts which were intended to coordinate participation
in the April 1st special subreddit /r/place.

These scripts work but it seems that new accounts are not allowed to
participate. I have been able to run these scripts with my main account
but I'd need several hundreds or even thousands of accounts in order
to be able to draw the image that I would like :(

![Spiral](https://raw.githubusercontent.com/eriknstr/mr_fourchan/master/res/mr_fourchan_16.png)

## User accounts

Put user accounts and passwords in the file `created.txt`.

The format is *username* &lt;tab&gt; *passphrase*.

One pair per line.

## Prepare target bitmap data

```bash
mkdir -p tmp remote
./png2place.py res/mr_fourchan_16.png tmp/mr_fourchan_16.bin
```

Verify that transformations work as intended.

```bash
./place2png.bash tmp/mr_fourchan_16.bin tmp/mr_fourchan_16.png
feh tmp/mr_fourchan_16.png
./png2place.py tmp/mr_fourchan_16.png tmp/mr_fourchan_16_again.bin
diff tmp/mr_fourchan_16.bin tmp/mr_fourchan_16_again.bin
rm tmp/mr_fourchan_16_again.bin
```

## Download current bitmap

```bash
./dl.bash
```

## Keep downloading more

Run this in a separate terminal or w/e.

```bash
while true ; do ./dl.bash ; sleep 60 ; done
```

## Convert the downloaded bitmap to PNG

In case you want to look at it. Useful for verification as well.

```bash
latestbin="$( ls remote/ | tail -n1 )"
./place2png.bash "remote/$latestbin" "tmp/${latestbin%.bin}.png"
```

## Convert all downloaded bitmaps to PNG

```bash
./pngall.bash
```

## Perform work

```bash
./le_loop.bash
```
