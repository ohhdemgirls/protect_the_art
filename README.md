# Protect the Art

Scripts for coordinated participation in April 1st special subreddit /r/place

Rewrite in progress!

## Create directories for data

```bash
mkdir -p tmp remote
```

## Prepare target bitmap data

Use your own 1000x1000 PNG in place of `sample/mr_fourchan_16.png` if you
desire.  Note that the palette of the PNG *must* match the /r/place pallette.
See the file `palette.py` for a listing of the 16 palette colors.

While the file needs to be 1000x1000 pixels, you don't need to fill all of
it with artwork. If for example you are only interested in mantaining say
a 32x24 region at some offset, paint that portion into the PNG at the
desired location and note the pixel positions of the upper left and the
lower right hand corners of your artwork area.

```bash
./png2place.py sample/mr_fourchan_16.png tmp/mr_fourchan_16.bin
```

Verify that transformations work as intended.

```bash
./place2png.bash tmp/mr_fourchan_16.bin tmp/mr_fourchan_16.png
feh tmp/mr_fourchan_16.png &
./png2place.py tmp/mr_fourchan_16.png tmp/mr_fourchan_16_again.bin
diff tmp/mr_fourchan_16.bin tmp/mr_fourchan_16_again.bin && \
  rm tmp/mr_fourchan_16_again.bin
```

## Authenticate user accounts

Put user accounts and passwords in a file named `accounts.txt`.

The format is *username* &lt;tab&gt; *passphrase*.

One pair per line.

Once you have created the accounts, run
the authentication script to get cookies.

```bash
./auth.py accounts.txt
```

## Monitor and maintain artwork

Let this script run for as long as you wish to participate.

Replace `tmp/mr_fourchan_16.bin` with the name of the
binary data file created above if you used your own 1000x1000 PNG.

If you wish to contribute to maintaining the first region, run:

```bash
./continuous.py 9 12 745 26 tmp/mr_fourchan_16.bin
```

The arguments to the `continuous.py` script are as follows:

1. Start x -- the x-coordinate of the upper left hand corner.
2. Start y -- the y-coordinate of the upper left hand corner.
3. End x -- the x-coordinate of the lower right hand corner.
4. End y -- the y-coordinate of the lower right hand corner.
5. The name of the binary file produced by the `png2place.py` script.

If you wish to contribute to maintaining the full artwork,
the origin and end x and y coordinate arguments can be omitted.

## Optional: Convert the most recently downloaded bitmap to PNG

In case you want to look at it. Useful for verification as well.

```bash
latestbin="$( ls remote/ | tail -n1 )"
./place2png.bash "remote/$latestbin" "tmp/${latestbin%.bin}.png"
```

## Optional: Convert all downloaded bitmaps to PNG

```bash
./pngall.bash
```
