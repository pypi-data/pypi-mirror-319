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
    im = cg.Image.get("https://images.pexels.com/photos/2379005/pexels-photo-2379005.jpeg?cs=srgb&dl=pexels-italo-melo-881954-2379005.jpg&fm=jpg&w=640&h=800")
    return (im,)


@app.cell
def _(im):
    im
    return


@app.cell
def _(cg):
    pipeline = cg.pipeline("face-detection")
    return (pipeline,)


@app.cell
def _(im, pipeline):
    faces_im = pipeline(im)
    return (faces_im,)


@app.cell
def _(faces_im):
    faces_im
    return


@app.cell
def _(faces_im):
    faces = faces_im.top
    return (faces,)


@app.cell
def _(faces):
    faces
    return


@app.cell
def _(faces):
    faces[0].image()
    return


@app.cell
def _(faces):
    faces[0].image().plot(scale=4)
    return


@app.cell
def _(cg):
    im2 = cg.Image.get("https://images.pexels.com/photos/109919/pexels-photo-109919.jpeg").resize(1600)
    return (im2,)


@app.cell
def _(im2):
    im2
    return


@app.cell
def _(im2, pipeline):
    faces_im2 = pipeline(im2)
    return (faces_im2,)


@app.cell
def _(faces_im2):
    faces_im2
    return


@app.cell
def _(faces_im2):
    faces_im2.top[1].image().plot(scale=4)
    return


if __name__ == "__main__":
    app.run()
