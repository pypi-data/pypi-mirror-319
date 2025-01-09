import napari
import tifffile
import itk
import random, math
import numpy as np
import pathlib
import os, glob, csv
import napari_3dtimereg.Utils as ut
from skimage.measure import label, regionprops
from magicgui import magicgui
from napari.utils.history import get_save_history, update_save_history
from webbrowser import open_new_tab

"""
Napari - 3D Time Reg

Napari plugin to do movie registration with possible deformation. Uses elastix library.
Registration is calculated on one reference chanel and applied to the others.

author: Gaëlle Letort, CNRS/Institut Pasteur
"""

def get_filename():
    """ User selection of movie to process """
    from qtpy.QtWidgets import QFileDialog
    dialog = QFileDialog(caption="Choose reference image")
    hist = get_save_history()
    dialog.setHistory(hist)
    dialog.setFileMode(QFileDialog.ExistingFile)
    dialog.setDirectory(hist[0])
    if dialog.exec_():
        filename = dialog.selectedFiles()
    if filename:
        return filename[0]
    else:
        return None

def start():
    global viewer
    viewer = napari.current_viewer()
    viewer.title = "3dTimeReg"
    filename = get_filename()
    if filename is None:
        print("No file selected")
        return
    open_file( filename )
    return getChanels()

def start_noshow():
    global viewer
    viewer = None
    #viewer = napari.Viewer( show=False )

def open_file( filename, show_images=True ):
    global refimg, refchanel
    global imagename
    global resimg
    global scaleXY, scaleZ
    global aligndir, imagedir 
    global colchan, dim
    global refpts
    refpts = None
    refchanel = 0
    refimg, scaleXY, scaleZ, names = ut.open_image(filename, verbose=True)
    global pixel_spacing
    pixel_spacing = [1, 1]
    if (scaleZ is not None) and (scaleZ>0):
        pixel_spacing.append(scaleZ/scaleXY)
    print("Image size: "+str(refimg.shape))
    print("Scale: "+str(pixel_spacing))

    ## test if 2d or 3d movie (several chanels assumed)
    if len(refimg.shape)==4:
        colchan = 1
        dim = 2
        scaleZ = -1
    else:
        colchan = 2
        dim = 3
    imagename, imagedir, aligndir = ut.extract_names( filename, subname="aligned" )
    if show_images:
        update_save_history(imagedir)
        for chan in range(refimg.shape[colchan]):
            cmap = ut.colormapname(chan)
            if dim == 3:
                cview = viewer.add_image( refimg[:,:,chan,:,:], name="Movie_"+"C"+str(chan), blending="additive", colormap = cmap )
                quants = tuple( np.quantile( refimg[:,:,chan,:,:], [0.01, 0.9999]) )
            else:
                cview = viewer.add_image( refimg[:,chan,:,:], name="Movie_"+"C"+str(chan), blending="additive", colormap = cmap )
                quants = tuple( np.quantile( refimg[:,chan,:,:], [0.01, 0.9999]) )
            cview.contrast_limits = quants
            cview.gamma = 0.95
    

def show_help_chanel():
    """ Open the gitlab page with the documentation """
    import webbrowser
    webbrowser.open_new_tab("https://gitlab.pasteur.fr/gletort/napari-3dtimereg/#choose-movie-and-reference-chanel")
    return

def show_help_align():
    """ Open the gitlab page with the documentation """
    import webbrowser
    webbrowser.open_new_tab("https://gitlab.pasteur.fr/gletort/napari-3dtimereg/#calculate-alignement")
    return

def getChanels():
    """ Choose the chanel on which to calculate the alignement """

    @magicgui(call_button="Update", 
            reference_chanel={"widget_type": "Slider", "min":0, "max": refimg.shape[2]-1}, 
            help={"widget_type":"PushButton", "value": False, "name": "help"}, 
            )
    def get_chanel( reference_chanel=0 , help=False, ):
        global refchanel
        global resimg
        global colchan
        viewer.window.remove_dock_widget("all")
        refchanel = reference_chanel
        for chan in range(refimg.shape[0]):
            layname = "Movie_"+"C"+str(chan)
            if chan != refchanel:
                if layname in viewer.layers:
                    viewer.layers.remove(layname)
            else:
                viewer.layers.remove(layname) ## tmp

        if "Do registration" not in viewer.window._dock_widgets:
            if dim == 2:
                resimg = np.copy(refimg[:,refchanel,:,:])
            else:
                resimg = np.copy(refimg[:,:,refchanel,:,:])
            resimg[0] = resimg[0] - np.min(resimg[0])
            cview = viewer.add_image( resimg, name="ResMovie", blending="additive", colormap = "red") 
            #quants = tuple( np.quantile( resimg, [0.01, 0.9999]) )
            #cview.contrast_limits = quants
            iterative_registration()
    
    get_chanel.help.clicked.connect(show_help_chanel)
    wid = viewer.window.add_dock_widget(get_chanel, name="Choose chanel")
    return wid

def getChanels_noshow( reference_chanel=0 ):
    """ Do the chanel step without interface """
    global refchanel
    global resimg
    global colchan
    refchanel = reference_chanel
    
    if dim == 2:
        resimg = np.copy(refimg[:,refchanel,:,:])
    else:
        resimg = np.copy(refimg[:,:,refchanel,:,:])
        resimg[0] = resimg[0] - np.min(resimg[0])


def itk_to_layer(img, name, color):
    lay = layer_from_image(img)
    lay.blending = "additive"
    lay.colormap = color
    lay.name = name
    viewer.add_layer( lay )
        
def img_to_itk(img):
    """ Convert image array to itk image """
    image_itk = itk.GetImageFromArray(img)
    #fimage = itk.image_view_from_array((resimg[0]))
    image_itk.SetSpacing( tuple( [float(v) for v in pixel_spacing] ) )
    image_itk = image_itk.astype(itk.F)
    return image_itk

def rigid_map( iterations, rig_resolution, rig_final_spacing, use_points=True ):
    """ Set-up rigid (affine) transformation parameters """     
    parameter_object = itk.ParameterObject.New()
    parameter_map_rigid = parameter_object.GetDefaultParameterMap('rigid')
    parameter_map_rigid['MaximumNumberOfIterations'] = [iterations]
    parameter_map_rigid['MaximumStepLength'] = ['2.0']
    parameter_map_rigid["NumberOfResolutions"] = [rig_resolution]
    parameter_map_rigid['NumberOfSpatialSamples'] = ['10000']
    parameter_map_rigid['MaximumNumberOfSamplingAttempts'] = ['8']
    parameter_map_rigid['RequiredRatioOfValidSamples'] = ['0.05']
    parameter_map_rigid['CheckNumberOfSamples'] = ['false']
    parameter_map_rigid['FinalGridSpacingInPhysicalUnits'] = [str(rig_final_spacing)]
    parameter_map_rigid['Registration'] = ['MultiMetricMultiResolutionRegistration']
    parameter_map_rigid["AutomaticTransformInitialization"] = ['true']
    parameter_map_rigid["AutomaticTransformInitializationMethod"] = ['CenterOfGravity']
        
    original_metric = parameter_map_rigid['Metric']    
    if use_points==True:
        parameter_map_rigid['Metric'] = [original_metric[0], 'CorrespondingPointsEuclideanDistanceMetric']
        
    return parameter_map_rigid

def bspline_map( spline_resolution, iterations, final_order, spline_final_spacing ):
    """ Set-up bspline transformation parameters """
    preset = "bspline"
    parameter_object = itk.ParameterObject.New()
    parameter_map = parameter_object.GetDefaultParameterMap(preset)
        
    parameter_map["NumberOfResolutions"] = [spline_resolution]
    parameter_map["WriteIterationInfo"] = ["false"]
    parameter_map['MaximumStepLength'] = ['2.0']
    parameter_map['NumberOfSpatialSamples'] = ['8000']
    parameter_map['MaximumNumberOfSamplingAttempts'] = ['10']
    parameter_map['RequiredRatioOfValidSamples'] = ['0.05']
    parameter_map['MaximumNumberOfIterations'] = [iterations]
    parameter_map['FinalBSplineInterpolationOrder'] = [final_order]
    parameter_map['BSplineInterpolationOrder'] = ['2']
    parameter_map['HowToCombineTransform'] = ['Compose']
    nres = int(spline_resolution)
    spaces = []
    for step in range(nres):
        spaces.append( math.pow(2, nres-1-step) )
    parameter_map['GridSpacingSchedule'] = [str(v) for v in spaces ]
    parameter_map['FinalGridSpacingInPhysicalUnits'] = [str(v) for v in [spline_final_spacing]*int(spline_resolution)]

    return parameter_map

def time_registration( do_rigid, do_bspline, iterations, rigid_resolution, rigid_final_spacing, use_reference_points, spline_resolution, spline_final_spacing, final_order, show_log=True ):
    """ Go for frame by frame registration """
        
    ## Build registration parameter maps from GUI parameters
    registration_parameter_object = itk.ParameterObject.New()
    nmap = 0
    if do_rigid:
        pmap_rigid = rigid_map( iterations=str(iterations), rig_resolution=str(rigid_resolution), rig_final_spacing=int(rigid_final_spacing), use_points=use_reference_points )
        registration_parameter_object.AddParameterMap(pmap_rigid)
        nmap = nmap + 1
    if do_bspline:
        pmap_spline = bspline_map( spline_resolution=str(spline_resolution), iterations=str(iterations), final_order=str(final_order), spline_final_spacing=int(spline_final_spacing) )
        registration_parameter_object.AddParameterMap(pmap_spline)
        nmap = nmap + 1
            
    ## apply "alignement" to first frame
    apply_registration(0, None)

    # initialise a parameter object to which the transforms will be appended that result from the pairwise slice registrations
    curr_transform_object = itk.ParameterObject.New()

    # the first fixed image will be the reference slice
    fixed_image_itk = img_to_itk(resimg[0])

    ## Register all frames to previous one and add it
    for t in range(resimg.shape[0]):
        print("Calculate registration for time point "+str(t))

        if t > 0:
            # the moving image is the current slice
            moving_image_itk = img_to_itk(resimg[t])

            # perform the pairwise registration between two slices
            elastix_object = itk.ElastixRegistrationMethod.New(fixed_image_itk, moving_image_itk)
            elastix_object.SetParameterObject(registration_parameter_object)
            
            if use_reference_points:
                get_ref_points(t-1, t)
                elastix_object.SetFixedPointSetFileName(os.path.join(aligndir, imagename+"_refpts_fixed.txt"))
                elastix_object.SetMovingPointSetFileName(os.path.join(aligndir, imagename+"_refpts_moving.txt"))
            
            elastix_object.SetLogToConsole( show_log==True )

            # Update filter object (required)
            elastix_object.UpdateLargestPossibleRegion()

            # Results of Registration
            #affimage = elastix_object.GetOutput()
            results_transform_parameters = elastix_object.GetTransformParameterObject()

            # set the current moving image as the fixed image for the registration in the next iteration
            fixed_image_itk = moving_image_itk

            # append the obtained transform to the transform parameter object
            for i in range(nmap):
                curr_transform_object.AddParameterMap(results_transform_parameters.GetParameterMap(i))

            # transform the current slice and append it to the reconstructed stack
            apply_registration(t, curr_transform_object)

def middle_time_registration( do_rigid, do_bspline, iterations, rigid_resolution, rigid_final_spacing, use_reference_points, spline_resolution, spline_final_spacing, final_order, show_log=True ):
    """ Go for frame by frame registration, reference frame middle one """
        
    ## Build registration parameter maps from GUI parameters
    registration_parameter_object = itk.ParameterObject.New()
    nmap = 0
    if do_rigid:
        pmap_rigid = rigid_map( iterations=str(iterations), rig_resolution=str(rigid_resolution), rig_final_spacing=int(rigid_final_spacing), use_points=use_reference_points )
        registration_parameter_object.AddParameterMap(pmap_rigid)
        nmap = nmap + 1
    if do_bspline:
        pmap_spline = bspline_map( spline_resolution=str(spline_resolution), iterations=str(iterations), final_order=str(final_order), spline_final_spacing=int(spline_final_spacing) )
        registration_parameter_object.AddParameterMap(pmap_spline)
        nmap = nmap + 1
            
    ## reference frame
    reft = int( resimg.shape[0]/2 )

    ## apply "alignement" to first frame
    apply_registration(reft, None)

    # initialise a parameter object to which the transforms will be appended that result from the pairwise slice registrations
    curr_transform_object = itk.ParameterObject.New()

    # the first fixed image will be the reference slice
    fixed_image_itk = img_to_itk(resimg[reft])

    ## Register all frames to following one and add it
    t = reft - 1
    while t >= 0:
        print("Calculate registration for time point "+str(t))

        # the moving image is the current slice
        moving_image_itk = img_to_itk(resimg[t])

        # perform the pairwise registration between two slices
        elastix_object = itk.ElastixRegistrationMethod.New(fixed_image_itk, moving_image_itk)
        elastix_object.SetParameterObject(registration_parameter_object)
            
        if use_reference_points:
            get_ref_points(t+1, t)
            elastix_object.SetFixedPointSetFileName(os.path.join(aligndir, imagename+"_refpts_fixed.txt"))
            elastix_object.SetMovingPointSetFileName(os.path.join(aligndir, imagename+"_refpts_moving.txt"))
            
        elastix_object.SetLogToConsole( show_log==True )

        # Update filter object (required)
        elastix_object.UpdateLargestPossibleRegion()

        # Results of Registration
        results_transform_parameters = elastix_object.GetTransformParameterObject()

        # set the current moving image as the fixed image for the registration in the next iteration
        fixed_image_itk = moving_image_itk

        # append the obtained transform to the transform parameter object
        for i in range(nmap):
            curr_transform_object.AddParameterMap(results_transform_parameters.GetParameterMap(i))

        # transform the current slice and append it to the reconstructed stack
        apply_registration(t, curr_transform_object)

        ## next time
        t = t - 1
   
    ## Next phase go from refframe to the end
    t = reft + 1
    fixed_image_itk = img_to_itk(resimg[reft])
    curr_transform_object = itk.ParameterObject.New()
    while t < resimg.shape[0]:
        print("Calculate registration for time point "+str(t))

        # the moving image is the current slice
        moving_image_itk = img_to_itk(resimg[t])

        # perform the pairwise registration between two slices
        elastix_object = itk.ElastixRegistrationMethod.New(fixed_image_itk, moving_image_itk)
        elastix_object.SetParameterObject(registration_parameter_object)
            
        if use_reference_points:
            get_ref_points(t-1, t)
            elastix_object.SetFixedPointSetFileName(os.path.join(aligndir, imagename+"_refpts_fixed.txt"))
            elastix_object.SetMovingPointSetFileName(os.path.join(aligndir, imagename+"_refpts_moving.txt"))
            
        elastix_object.SetLogToConsole( show_log==True )

        # Update filter object (required)
        elastix_object.UpdateLargestPossibleRegion()

        # Results of Registration
        results_transform_parameters = elastix_object.GetTransformParameterObject()

        # set the current moving image as the fixed image for the registration in the next iteration
        fixed_image_itk = moving_image_itk

        # append the obtained transform to the transform parameter object
        for i in range(nmap):
            curr_transform_object.AddParameterMap(results_transform_parameters.GetParameterMap(i))

        # transform the current slice and append it to the reconstructed stack
        apply_registration(t, curr_transform_object)

        ## next time
        t = t + 1

def iterative_registration():
    """ use Elastix to perform registration with possible deformation, iteratively in time """     
    
    @magicgui(call_button="Go", 
            rigid_resolution={"widget_type":"LiteralEvalLineEdit"}, 
            spline_resolution={"widget_type":"LiteralEvalLineEdit"}, 
            iterations={"widget_type":"LiteralEvalLineEdit"}, 
            rigid_final_spacing={"widget_type":"LiteralEvalLineEdit"}, 
            spline_final_spacing={"widget_type":"LiteralEvalLineEdit"}, 
            final_order={"widget_type":"LiteralEvalLineEdit"}, 
            help={"widget_type":"PushButton", "value": False, "name": "help"}, 
            )
    def get_paras( 
            show_log = True,
            use_reference_points = False,
            refpoints_file = pathlib.Path(os.path.join(imagedir, imagename+"_reference_points.csv")),
            do_rigid = True,
            do_bspline = True,
            middle_reference_frame = True,
            show_advanced_parameters = False,
            rigid_resolution=4,
            spline_resolution=4,
            iterations=1000,
            rigid_final_spacing=50, 
            spline_final_spacing=50, 
            final_order = 1,
            help = False,
            ):
        
        global move_points
        reslay = viewer.layers["ResMovie"]
        #use_reference_points = False
        if use_reference_points:
            read_points( refpoints_file )
            #move_points = True 
        if not middle_reference_frame:
            time_registration( do_rigid=do_rigid, do_bspline=do_bspline, iterations=iterations, rigid_resolution=rigid_resolution, rigid_final_spacing=rigid_final_spacing, use_reference_points=use_reference_points, spline_resolution=spline_resolution, spline_final_spacing=spline_final_spacing, final_order=final_order, show_log=show_log )
        else:
            middle_time_registration( do_rigid=do_rigid, do_bspline=do_bspline, iterations=iterations, rigid_resolution=rigid_resolution, rigid_final_spacing=rigid_final_spacing, use_reference_points=use_reference_points, spline_resolution=spline_resolution, spline_final_spacing=spline_final_spacing, final_order=final_order, show_log=show_log )
        finish_image()
    
    def show_advanced(booly):
        get_paras.spline_resolution.visible = (booly and get_paras.do_bspline.value)
        get_paras.rigid_resolution.visible = (booly and get_paras.do_rigid.value)
        get_paras.iterations.visible = booly
        get_paras.rigid_final_spacing.visible = (booly and get_paras.do_rigid.value)
        get_paras.spline_final_spacing.visible = (booly and get_paras.do_bspline.value)

    def show_spline():
        get_paras.final_order.visible = get_paras.do_bspline.value

    show_advanced(False)
    show_spline()
    get_paras.show_advanced_parameters.changed.connect(show_advanced)
    get_paras.do_bspline.changed.connect(show_spline)
    get_paras.do_bspline.changed.connect(show_advanced)
    get_paras.do_rigid.changed.connect(show_advanced)
    get_paras.help.clicked.connect(show_help_align)
    wid = viewer.window.add_dock_widget(get_paras, name="Calculate alignement")

    
def read_points( refpoints_file ):
    """ Read the TrackMate file containing all the points coordinates """
    global refpts
    global move_points
    move_points = False
    ptsfile = refpoints_file
    if not os.path.exists(ptsfile):
        print("Reference points file "+ptsfile+" not found")
    refpts = []
    with open(ptsfile, "r") as infile:
        csvreader = csv.DictReader(infile)
        for row in csvreader:
            cres = []
            if row["TrackID"].isdigit():
                for col in ["TrackID", "X", "Y", "Z", "T"]:
                    cres.append(int(float(row[col])))
                refpts.append(cres)
    refpts = np.array(refpts)
    
def get_ref_points(time0, time1):
    """ Get the reference points common between time0 and time1 and put them to file """
    global refpts
    pttime0 = refpts[refpts[:,4]==time0,]
    pttime1 = refpts[refpts[:,4]==time1,]
    inter, ind1, ind0 = np.intersect1d(pttime1[:,0], pttime0[:,0], return_indices=True)
    write_ref_file(ind1, pttime1, "moving")
    write_ref_file(ind0, pttime0, "fixed")

def get_closest_label(pts, tid):
    """ Find closest pt id to tid """
    closest = pts[0]
    dist = 1000
    for pt in pts:
        d = abs(pt[0]-tid)
        if d < dist:
            dist = d
            closest = pt
    return closest
    
def update_points(mask, time):
    """ Update the points coordinates at time from the mask """
    global refpts
    pttime = refpts[refpts[:,4]==time,]
    masknp = itk.array_from_image(mask)
    masknp[masknp<0] = 0
    masknp = np.array(masknp)
        #res = res - np.min(res)
    #masknp = masknp
    masknp = np.ceil(masknp)
    print(np.unique(masknp))
    masknp = np.uint16(masknp)
    print(np.unique(masknp))
    lab = label(masknp)
    props = regionprops(lab, masknp)
    if len(props) != len(pttime):
        print(len(props))
        print(len(pttime))
        print("Point missing ?????")
        print(pttime)
        print(props)
    print(pttime)
    for prop in props:
        cent = prop.centroid
        tid = prop.intensity_max-20
        pt = get_closest_label(pttime, tid)
        print(tid)
        print(pt)
        #print(cent)
        pt[1] = cent[1]
        pt[2] = cent[2]
        pt[3] = cent[0]
        #print(pt)

def points_to_mask(time):
        """ Get the reference points and put them to image """
        global refpts
        pttime = refpts[refpts[:,4]==time,]
        if dim == 2:
            imshape = refimg.shape[2:4]
        else:
            imshape = (refimg.shape[1],)+refimg.shape[3:5]
            print(imshape)
        img = np.zeros( imshape, np.uint8)
        for pt in pttime:
            img[ pt[3], pt[2], pt[1] ] = (pt[0]+20)  ## put the label value
            print(pt)
        return img

def write_ref_file(inds, pts, fixed):
    """ Write points of inds in file for time """
    filepath = os.path.join(aligndir, imagename+"_refpts_"+fixed+".txt")
    f = open(filepath, "w")
    f.write("index\n")
    f.write(str(len(inds))+"\n")
    for ind in inds:
        pt = pts[ind,]
        y = pt[2]
        #if imsize is not None:
        #    y = imsize - pt[1]
        f.write(str(int(pt[1]))+" "+str(int(y))+" "+str(int(pt[3]))+"\n")
        #f.write(str(y)+" "+str(pt[1])+"\n")
    f.close()
    
def save_points():
    """ Save updated points coordinates """
    global refpts
    outfile = os.path.join(aligndir, imagename+"_refpts_moved.csv")
    with open(outfile, "w") as infile:
        csvwriter = csv.writer(infile)
        csvwriter.writerow(["TrackID", "X", "Y", "Z", "T"])
        csvwriter.writerows( refpts.tolist())

def layer_from_image(img):
    data = np.array(itk.array_view_from_image(img))
    image_layer = napari.layers.Image(data)
    return image_layer

def save_images(time):
    """ Save all chanels unmoved of frame time """
    global dim
    if dim == 3:
        chanellist = list(range(refimg.shape[2]))
    else:
        chanellist = list(range(refimg.shape[1]))
    for chan in chanellist:
        if dim == 3:
            res = np.copy(refimg[time,:,chan,:,:])
            #res = res - np.min(res)
            res = np.uint16(res)
            ut.writeTif( res, os.path.join(aligndir, imagename+"_C"+str(chan)+"_T"+"{:04d}".format(time)+".tif"), scaleXY, scaleZ, "uint16" )
        else:
            res = np.copy(refimg[time,chan,:,:])
            #res = res - np.min(res)
            res = np.uint16(res)
            ut.writeTif( res, os.path.join(aligndir, imagename+"_C"+str(chan)+"_T"+"{:04d}".format(time)+".tif"), scaleXY, -1, "uint16" )

def apply_registration(time, results_transform):
    """ Apply caclulated registration to the other chanels """
    global dim
    global move_points
    if dim == 2:
        align_chanels = list(range(refimg.shape[1]))
    else:
        align_chanels = list(range(refimg.shape[2]))

    print("Apply alignment to "+str(align_chanels))
    pt_image = None
    moved_pts = False

    for chan in align_chanels:
        if dim == 2:
            img = refimg[time,chan,:,:]
        else:
            img = refimg[time,:,chan,:,:]
        res = []
        itkimage = img_to_itk(img)
        ImageType = itk.Image[itk.F, dim]
        
        if results_transform is not None:
            transformix = itk.TransformixFilter[ImageType].New()
            transformix.SetMovingImage(itkimage)
            transformix.SetTransformParameterObject(results_transform)
            res_image = transformix.GetOutput()
            #if (not moved_pts) and move_points:
            #    if pt_image is None:
            #        ptimg = points_to_mask(time)
            #        pt_image = itk.image_view_from_array(ptimg)
            #        pt_image = pt_image.astype(itk.F)
                #transformix.SetMovingImage(itkimage)
                #transformix.SetTransformParameterObject(results_transform_parameters)
                #pt_image = transformix.GetOutput()
                #resclayerm = layer_from_image(pt_image)
                #resclayerm.blending = "additive"
                #resclayerm.name = "MovingPointsAfter"
                #viewer.add_layer( resclayerm )
            #res = itk.array_from_image(res_image)
            res = np.array(res_image)
        else:
            res = img

        res[res<0] = 0
        res = np.array(res)
        #res = res - np.min(res)
        res = np.uint16(res)

        #if pt_image is not None:
        #    update_points(pt_image, time)
        
        ut.writeTif( res, os.path.join(aligndir, imagename+"_C"+str(chan)+"_T"+"{:04d}".format(time)+".tif"), scaleXY, scaleZ, "uint16" )

def finish_image():
    """ End, create composite image """
    global movimg, refpts
    if refpts is not None:
        save_points()
    remove_widget("Calculate alignement")
    remove_layer("ResMovie")
    create_result_image()

def remove_layer(layname):
    if layname in viewer.layers:
        viewer.layers.remove(layname)

def remove_widget(widname):
    if widname in viewer.window._dock_widgets:
        wid = viewer.window._dock_widgets[widname]
        wid.setDisabled(True)
        del viewer.window._dock_widgets[widname]
        wid.destroyOnClose()

def create_result_image():
    """ Create one final composite movies of aligned images """
    
    @magicgui(call_button = "Concatenate aligned images",)
    def get_files():
        save_result_image()
    viewer.window.add_dock_widget(get_files, name="Concatenate")

def save_result_image():
    resimg = np.zeros(refimg.shape) 
    if dim == 2:
        nchans = refimg.shape[1]
    else:
        nchans = refimg.shape[2]

    for chan in range(nchans):
        for time in range(refimg.shape[0]):
            filename = os.path.join(aligndir, imagename+"_C"+str(chan)+"_T"+"{:04d}".format(time)+".tif")
            img, tscaleXY, tscaleZ, names = ut.open_image(filename, verbose=False)
            if dim == 2:
                resimg[time, chan, :,:] = img
            else:
                resimg[time, :, chan, :,:] = img
            os.remove(filename)

    if viewer is not None:
        viewer.add_image(resimg, name="Res", blending="additive")
        for lay in viewer.layers:
            if lay.name != "Res":
                remove_layer(lay)
    imgname = os.path.join(aligndir, imagename+".tif")
    resimg = np.array(resimg, "uint16")
    # move the chanel axis after the Z axis (imageJ format)
    if dim == 3:
        resimg = np.moveaxis(resimg, 0, 1)
        print(resimg.shape)
        tifffile.imwrite(imgname, resimg, imagej=True, resolution=[1./scaleXY, 1./scaleXY], metadata={'PhysicalSizeX': scaleXY, 'spacing': scaleZ, 'unit': 'um', 'axes': 'TZCYX'})
    else:
        tifffile.imwrite(imgname, resimg, imagej=True, resolution=[1./scaleXY, 1./scaleXY], metadata={'PhysicalSizeX': scaleXY, 'unit': 'um', 'axes': 'TCYX'})
    print("Image "+imgname+" saved")
    

