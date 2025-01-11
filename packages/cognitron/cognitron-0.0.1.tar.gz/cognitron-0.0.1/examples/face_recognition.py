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
    video = cg.Video.example("moldtech_ppvc_subesp_corporativo.mp4")
    return (video,)


@app.cell
def _(video):
    video
    return


@app.cell
def _(video):
    im1 = video.extract_frame(16)
    im1
    return (im1,)


@app.cell
def _(video):
    im2 = video.extract_frame(24)
    im2
    return (im2,)


@app.cell
def _(cg):
    p_det = cg.pipeline("face-detection")
    p_rec = cg.pipeline("face-recognition")
    return p_det, p_rec


@app.cell
def _(im1, p_det):
    im1_faces = p_det(im1)
    im1_faces
    return (im1_faces,)


@app.cell
def _(im1_faces):
    face1 = im1_faces.top[0]
    type(face1)
    return (face1,)


@app.cell
def _(face1):
    face1.image()
    return


@app.cell
def _(face1, p_rec):
    face1.embedding(p_rec)
    return


@app.cell
def _(face1, im2, p_det, p_rec):
    import numpy as np

    def find_person(im, query):
        faces = p_det(im).top
        embeddings = [x.embedding(p_rec) for x in faces]
        i, score = query.nearest(embeddings)
        return im.box(faces[i].bbox, score=score)

    find_person(im2, face1.embedding(p_rec))
    return find_person, np


if __name__ == "__main__":
    app.run()
