import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import cognitron as cg
    return cg, mo


@app.cell
def _(cg):
    IMAGE_URL = "https://images.pexels.com/photos/2379005/pexels-photo-2379005.jpeg?cs=srgb&dl=pexels-italo-melo-881954-2379005.jpg&fm=jpg&w=640&h=800"

    im = cg.Image.get(IMAGE_URL)
    return IMAGE_URL, im


@app.cell
def _(im):
    im
    return


@app.cell
def _(im):
    im.resize(128)
    return


@app.cell
def _(im):
    im.resize(128).plot()
    return


@app.cell
def _(im):
    im.resize(128).plot(scale=2)
    return


@app.cell
def _(im):
    im.resize(128).plot(scale=4)
    return


@app.cell
def _(im):
    im.box(0.2, 0.1, 0.6, 0.8, label="example")
    return


@app.cell
def _(im):
    im.affine(size=im.size, matrix=[
        [1, 0, 20],
        [0.1, 1, 0]])
    return


if __name__ == "__main__":
    app.run()
