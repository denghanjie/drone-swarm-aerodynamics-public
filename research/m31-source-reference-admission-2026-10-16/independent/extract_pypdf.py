"""Read-only Figure 7 vector extraction with pypdf; no physical analysis.

PRIVATE-FULL-PATHS.json must stay private. Public handoff files contain only
visible original vertices and a separately labeled clipped display endpoint.
"""
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
import pypdf
from pypdf import PdfReader
from pypdf.generic import ContentStream

PDF = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
EXPECTED = '81987dfd1cf2980270defd9447a9e5fb6c1586eab77b75b730de127c932d373c'
IDENTITY = [1, 0, 0, 1, 0, 0]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def save(name,value):
    with (OUT/name).open('x') as stream:
        json.dump(value,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')

def compose(old,new):
    a,b,c,d,e,f = old
    A,B,C,D,E,F = new
    return [a*A+c*B,b*A+d*B,a*C+c*D,b*C+d*D,a*E+c*F+e,b*E+d*F+f]

def point(matrix,x,y):
    a,b,c,d,e,f = matrix
    return [a*x+c*y+e,b*x+d*y+f]

pdf_bytes = PDF.read_bytes()
assert digest(pdf_bytes) == EXPECTED
reader = PdfReader(PDF)
page = reader.pages[4]
page_ops = ContentStream(page.get_contents(),reader).operations
ctm = IDENTITY[:]
stack = []
placements = []
for index,(operands,operator) in enumerate(page_ops):
    if operator == b'q': stack.append(ctm[:])
    elif operator == b'Q': ctm = stack.pop()
    elif operator == b'cm': ctm = compose(ctm,list(map(float,operands)))
    elif operator == b'Do': placements.append({'name':str(operands[0]),'opIndex':index,'ctm':ctm[:]})
placement = [x for x in placements if x['name'] == '/Im7']
assert len(placement) == 1
placement = placement[0]
form_ref = page['/Resources']['/XObject'].raw_get('/Im7')
form = form_ref.get_object()
form_matrix = list(map(float,form.get('/Matrix',IDENTITY)))
ops = ContentStream(form,reader).operations
resources = form['/Resources']
state = {'ctm':compose(placement['ctm'],form_matrix),'strokeColorSpace':'DeviceGray','strokeColor':[0.0],
         'fillColorSpace':'DeviceGray','fillColor':[0.0],'width':1.0,'strokeAlpha':1.0,'fillAlpha':1.0,
         'dash':[[],0.0],'clips':[]}
stack = []
path = []
paths = []
pending_clip = None
for index,(operands,operator) in enumerate(ops):
    op = operator.decode()
    if op == 'q': stack.append(copy.deepcopy(state))
    elif op == 'Q': state = stack.pop()
    elif op == 'cm': state['ctm'] = compose(state['ctm'],list(map(float,operands)))
    elif op in ['m','l','c','v','y']:
        vals = list(map(float,operands))
        path.append({'opIndex':index,'operator':op,'rawOperands':[str(x) for x in operands],
                     'raw':vals,'pagePoints':[point(state['ctm'],vals[k],vals[k+1]) for k in range(0,len(vals),2)],
                     'ctm':state['ctm'][:]})
    elif op == 're':
        x,y,w,h = map(float,operands)
        path.append({'opIndex':index,'operator':op,'rawOperands':[str(x) for x in operands],
                     'raw':[x,y,w,h],'pagePoints':[point(state['ctm'],X,Y) for X,Y in [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]],
                     'ctm':state['ctm'][:]})
    elif op == 'h': path.append({'opIndex':index,'operator':op,'raw':[],'pagePoints':[],'ctm':state['ctm'][:]})
    elif op in ['W','W*']: pending_clip = {'clipOperatorIndex':index,'rule':op,'commands':copy.deepcopy(path)}
    elif op in ['S','s','f','F','f*','B','B*','b','b*','n']:
        if op != 'n':
            paths.append({'id':'page5/Im7/paint-op-'+str(index),'paintOperatorIndex':index,'paintOperator':op,
                          'commands':copy.deepcopy(path),'stateAtPaint':copy.deepcopy(state)})
        if pending_clip:
            state['clips'].append(pending_clip)
            pending_clip = None
        path = []
    elif op in ['RG','rg','G','g','K','k']:
        prefix = 'stroke' if op.isupper() else 'fill'
        state[prefix+'ColorSpace'] = {'RG':'DeviceRGB','G':'DeviceGray','K':'DeviceCMYK'}[op.upper()]
        state[prefix+'Color'] = list(map(float,operands))
    elif op == 'w': state['width'] = float(operands[0])
    elif op == 'd': state['dash'] = [list(map(float,operands[0])),float(operands[1])]
    elif op == 'gs':
        gs = resources['/ExtGState'][operands[0]].get_object()
        if '/CA' in gs: state['strokeAlpha'] = float(gs['/CA'])
        if '/ca' in gs: state['fillAlpha'] = float(gs['/ca'])
assert not stack
by_op = {p['paintOperatorIndex']:p for p in paths}

axis = by_op[144]
axis_points = [c['raw'] for c in axis['commands'] if c['operator'] in ['m','l']]
xmin = min(x for x,y in axis_points)
xmax = max(x for x,y in axis_points)
ymin = min(y for x,y in axis_points)
ymax = max(y for x,y in axis_points)
assert (xmin,ymin) == (0.0,0.0)
assert (xmax,ymax) == (198.42685,99.21342)
axis_ctm = axis['commands'][0]['ctm']
assert axis_ctm[:4] == [1.0,0.0,0.0,1.0]
left,bottom = point(axis_ctm,0,0)
page_height = float(page.mediabox.height)
right,top = point(axis_ctm,xmax,ymax)

def normalized(x,y):
    return [3*(x-xmin)/(xmax-xmin),1.5*(y-ymin)/(ymax-ymin)]

def metadata(p):
    s = p['stateAtPaint']
    coords = [pt for c in p['commands'] for pt in c['pagePoints']]
    return {'pathID':p['id'],'paintOperatorIndex':p['paintOperatorIndex'],'paintOperator':p['paintOperator'],
            'firstPathOperatorIndex':p['commands'][0]['opIndex'],'commandCount':len(p['commands']),
            'strokeColorSpace':s['strokeColorSpace'],'strokeColor':s['strokeColor'],'strokeWidthPt':s['width'],
            'strokeAlpha':s['strokeAlpha'],'fillColorSpace':s['fillColorSpace'],'fillColor':s['fillColor'],
            'fillAlpha':s['fillAlpha'],'dash':s['dash'],
            'pageBoundsBottomOrigin':[min(v[0] for v in coords),min(v[1] for v in coords),max(v[0] for v in coords),max(v[1] for v in coords)],
            'activeClipOperatorIndices':[c['clipOperatorIndex'] for c in s['clips']]}

selected = [('Offboard 1',897,[0.85,0.325,0.098],1115,1135),('Offboard 2',941,[0.929,0.694,0.125],1153,1173)]
private = []
visible = []
for name,paint,color,legend_paint,legend_text in selected:
    p = by_op[paint]
    s = p['stateAtPaint']
    assert s['strokeColorSpace'] == 'DeviceRGB' and s['strokeColor'] == color
    assert p['paintOperator'] == 'S' and s['width'] == .79701 and s['strokeAlpha'] == 1
    assert s['clips'][-1]['clipOperatorIndex'] == 806
    assert all(c['operator'] in ['m','l'] and c['ctm'] == axis_ctm for c in p['commands'])
    vertices = []
    for index,c in enumerate(p['commands']):
        x,y = c['raw']
        page_x,page_y = c['pagePoints'][0]
        vertices.append({'vertexIndex':index,'operatorIndex':c['opIndex'],'operator':c['operator'],
                         'plotLocalPt':[x,y],'pageBottomOriginPt':[page_x,page_y],
                         'pageTopOriginPt':[page_x,page_height-page_y],
                         'normalizedRadius':normalized(x,y)[0],'normalizedSpeed':normalized(x,y)[1],
                         'insideDisplayedAxes':xmin <= x <= xmax and ymin <= y <= ymax,
                         'rawOperandStrings':c['rawOperands']})
    raw_record = {'series':name,'metadata':metadata(p),'ctm':axis_ctm,'vertices':vertices}
    private.append(raw_record)
    shown = [v for v in vertices if v['insideDisplayedAxes']]
    assert len(shown) == 16
    last = shown[-1]
    after = vertices[last['vertexIndex']+1]
    x0,y0 = last['plotLocalPt']; x1,y1 = after['plotLocalPt']
    fraction = (xmax-x0)/(x1-x0)
    yclip = y0+fraction*(y1-y0)
    clip_page = point(axis_ctm,xmax,yclip)
    clipped = {'type':'display_interpolation_at_clip_boundary','isOriginalVertex':False,'isAdditionalMeasurement':False,
               'normalizedRadius':3.0,'normalizedSpeed':normalized(xmax,yclip)[1],
               'plotLocalPt':[xmax,yclip],'pageBottomOriginPt':clip_page,
               'pageTopOriginPt':[clip_page[0],page_height-clip_page[1]],
               'betweenOriginalVertexIndices':[last['vertexIndex'],after['vertexIndex']],
               'sourceSegmentOperatorIndices':[last['operatorIndex'],after['operatorIndex']],
               'interpretation':'Linear interpolation of the encoded display segment where PDF clipping cuts it; not an original measurement vertex.'}
    public_metadata = metadata(p)
    public_metadata.pop('pageBoundsBottomOrigin')
    visible.append({'series':name,'pathMetadata':public_metadata,'legendPathMetadata':metadata(by_op[legend_paint]),
                    'legendTextOperatorIndex':legend_text,'legendTextExpected':name,
                    'rawFullPathCanonicalSHA256':digest(canonical(raw_record)),
                    'fullPathVertexCount':len(vertices),'visibleOriginalVertexCount':len(shown),
                    'visibleOriginalVertices':shown,'clippedDisplayEndpoint':clipped})

private_record = {'sourcePDFSHA256':EXPECTED,'purpose':'PRIVATE full vector paths, including hidden off-axis coordinates; do not redistribute.',
                  'paths':private}
save('PRIVATE-FULL-PATHS.json',private_record)
public_record = {'kind':'figure7-visible-median-coordinate-extraction','sourcePDFSHA256':EXPECTED,'page':5,
                 'figure':7,'method':'pypdf ContentStream operators and graphics-state CTM traversal',
                 'normalizedDownstreamStation':3.0,'xObservable':'r/l','yObservable':'normalized flow speed; caption identifies colored lines as medians',
                 'fullPathsPrivateArtifactSHA256':digest((OUT/'PRIVATE-FULL-PATHS.json').read_bytes()),
                 'series':visible,'physicalContrastsComputed':False,'modelsFit':False,'uncertaintyBandsConvertedToSEM':False}
save('VISIBLE-PROFILES.json',public_record)

xgrid = [c['raw'][0] for c in by_op[29]['commands'] if c['operator'] == 'm']
ygrid = [c['raw'][1] for c in by_op[53]['commands'] if c['operator'] == 'm']
xresid = [normalized(x,0)[0]-index*.5 for index,x in enumerate(xgrid)]
yresid = [normalized(0,y)[1]-index*.25 for index,y in enumerate(ygrid)]
fills = [metadata(p) for p in paths if p['paintOperator'] in ['f','f*'] and p['stateAtPaint']['fillColor'] in [[.85,.325,.098],[.929,.694,.125]]]
for item in fills:
    item.pop('pageBoundsBottomOrigin')
evidence = {'kind':'independent-extraction-admission-evidence','sourcePDFSHA256':EXPECTED,'page':5,'figure':7,
            'pypdfVersion':pypdf.__version__,'pageMediaBox':list(map(float,page.mediabox)),
            'pageRotation':int(page.get('/Rotate',0)),'pageDoPlacement':placement,
            'formObject':{'resourceName':'/Im7','objectNumber':form_ref.idnum,'generation':form_ref.generation,
                          'bbox':list(map(float,form['/BBox'])),'formMatrix':form_matrix,
                          'decodedStreamSHA256':digest(form.get_data()),'operationCount':len(ops)},
            'operatorIndexConvention':'Zero-based index in pypdf ContentStream.operations for page 5 /Im7 unless identified as page operator.',
            'axis':{'boundaryPath':metadata(axis),'plotLocalBoundsPt':[xmin,ymin,xmax,ymax],
                    'plotLocalToPageCTM':axis_ctm,'pageBottomOriginBoundsPt':[left,bottom,right,top],
                    'pageTopOriginBoundsPt':[left,page_height-top,right,page_height-bottom],
                    'xRange':[0,3],'yRange':[0,1.5],
                    'xMapping':'r_over_l = 3 * plot_local_x / 198.42685',
                    'yMapping':'normalized_speed = 1.5 * plot_local_y / 99.21342',
                    'xGridPaintOperator':29,'yGridPaintOperator':53,'xGridLocalPt':xgrid,'yGridLocalPt':ygrid,
                    'xTickValues':[0,.5,1,1.5,2,2.5,3],'yTickValues':[0,.25,.5,.75,1,1.25,1.5],
                    'xTickTextTJOperators':[512,530,554,572,596,614,638],
                    'yTickTextTJOperators':[656,674,698,722,746,764,788],
                    'xGridNormalizedResiduals':xresid,'yGridNormalizedResiduals':yresid,
                    'axisLabelEvidence':'Numeric endpoints and intermediate tick labels verified against pypdf page text and the private full-page render.'},
            'excludedMeasuredUncertaintyBandPaths':fills,
            'excludedFitPath':metadata(by_op[1390]),'excludedFitLegend':metadata(by_op[1231]),
            'fitStrokeColorOverrideEvidence':{'precedingRGOperator':1286,'effectiveBlackGOperator':1289,'effectiveColorSpace':'DeviceGray','effectiveColor':[0.0]},
            'captionEvidence':{'station':'normalized downstream s = 3.0','line':'median value',
                               'shading':'1 sigma uncertainty around the mean','blackLine':'turbulent-jet radial profile, equation (3)'},
            'extractionUncertainty':{'coordinateSource':'Encoded vector centerline vertices, not pixel digitization.',
                                     'rawPlotCoordinateDecimalResolutionPt':0.00001,
                                     'conditionalHalfLastDigitNormalizedX':0.000005*3/xmax,
                                     'conditionalHalfLastDigitNormalizedY':0.000005*1.5/ymax,
                                     'quantizationInterpretation':'Half-last-digit values assume nearest rounding in the PDF export; they are not measurement uncertainty or guaranteed error bounds on original data.',
                                     'strokeHalfWidthNormalizedX':.79701/2*3/xmax,
                                     'strokeHalfWidthNormalizedY':.79701/2*1.5/ymax,
                                     'strokeInterpretation':'Rendering footprint only; not statistical uncertainty. Centerline extraction is exact relative to the encoded path numbers.',
                                     'suggestedCrossExtractorCoordinateTolerance':1e-6,
                                     'crossExtractorToleranceMeaning':'A numerical coordinate-reconciliation tolerance, not physical measurement accuracy.'},
            'admission':{'visibleMedianCoordinateExtraction':True,'outOfWindowVerticesAdmittedForPublicAnalysis':False,
                         'clippedEndpointIsDisplayInterpolation':True,'rawMeasurementRecoveryEstablished':False,
                         'statisticalContrastAdmission':False,'physicalContrastComputed':False,
                         'limits':['Figure-derived medians only; no raw sample count, covariance or time dependence recovered.',
                                   'Shaded 1-sigma uncertainty is around the mean while colored lines are medians; no SEM transformation is justified.',
                                   'No extrapolation beyond visible axes. Hidden vector vertices stay private.',
                                   'No fitted curve substituted for a measured median.']}}
save('EXTRACTION-EVIDENCE.json',evidence)
print(json.dumps({'visibleOriginalVerticesPerSeries':[len(x['visibleOriginalVertices']) for x in visible],
                  'clippedEndpoints':2,'rawFullPathsRemainPrivate':True,'independentMechanism':'pypdf ContentStream / CTM',
                  'axisPageTopOriginBounds':evidence['axis']['pageTopOriginBoundsPt'],
                  'effectiveFitStrokeColor':evidence['excludedFitPath']['strokeColor'],
                  'physicalContrastsComputed':False}))
