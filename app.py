from flask import Flask
#from rhino3dm import *
import ghhops_server as hs

app = Flask(__name__)
hops = hs.Hops(app)


@hops.component(
    "/pointat",
    name="PointAt",
    description="Get point along curve",
    icon="icons/star.png",
    inputs=[
        hs.HopsCurve("Curve", "C", "Curve to evaluate"),
        hs.HopsNumber("t", "t", "Parameter on Curve to evaluate"),
    ],
    outputs=[
        hs.HopsPoint("P", "P", "Point on curve at t")
    ]
)
def pointat(curve, t):
    return curve.PointAt(t)


@hops.component(
    "/upper",
    name="uppercase",
    description="Get uppercase string",
    icon="icons/star.png",
    inputs=[
        hs.HopsString("String", "S", "Input string"),
    ],
    outputs=[
        hs.HopsString("Output", "O", "Uppercase string")
    ]
)
def testing(S):
    return S.upper()
