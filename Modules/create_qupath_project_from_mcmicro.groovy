import ij.gui.Wand
import qupath.lib.objects.PathObjects
import qupath.lib.regions.ImagePlane
import static qupath.lib.gui.scripting.QPEx.*
import ij.IJ
import ij.process.ColorProcessor
import qupath.imagej.processing.RoiLabeling
import qupath.imagej.tools.IJTools
import java.util.regex.Matcher
import java.util.regex.Pattern
import groovy.io.FileType
import java.awt.image.BufferedImage
import qupath.lib.images.servers.ImageServerProvider
import qupath.lib.gui.commands.ProjectCommands
import qupath.lib.gui.QuPathGUI
import ij.process.ImageProcessor
// Remove this if you don't need to generate new cell intensity measurements (it may be quite slow)
 import qupath.lib.analysis.features.ObjectMeasurements
 import qupath.lib.gui.tools.MeasurementExporter
 import qupath.lib.objects.PathCellObject
 import qupath.lib.objects.PathDetectionObject

// for loading csv file 
regionSet="reg"

dir_workflow=args[0]
// dir_workflow = "Y:/003 CODEX/MCMICRO/SMM_project/20230522_BR1010694BR1034362_Gonsalves_3_membrane"
// workflowDir=args[0]
//dir_workflow = "Y:/003 CODEX/MCMICRO/SMM_project/20230522_BR1010694BR1034362_Gonsalves_3_membrane"
dir_workflow = "Y:/003 CODEX/MCMICRO/SMM_project/20240126_BR1631006_Gonsalves_3_membrane"

//dir_workflow = "M:/Projects/Villasboas-CODEX/SMM/MCMICRO/20230522_BR1010694BR1034362_Gonsalves_3_membrane"


def dir_ome = dir_workflow + "/registration"
println("  Input OME.TIFFs: " + dir_ome)

def dir_masks = dir_workflow + "/segmentation"

println("  Input Labeled Masks: " + dir_masks)

def dir_project = dir_workflow + "/QUPATH"
println("  Output QuPath: " + dir_project)
// def outputPath=workflowDir+"/REPORTS/AllQuPathQuantification.tsv"
// println("  Quantifications: "+outputPath)

def file_marker_csv = dir_workflow + "/markers.csv"

// Load list of markers from markers.csv file 
def list_markers = []
list_markers_csv = new File(file_marker_csv).readLines()

list_markers_csv.each() { item ->
     list_items = item.split(",")
     name_channel =  list_items[2]
     //print name_channel
     
     if(!name_channel.contains("marker_name")){
         list_markers << name_channel
         }
    }
    
// set the channel names
String[] chan_names = new String[list_markers.size()];
for (int i = 0; i < list_markers.size(); i++) {
   chan_names[i] = list_markers[i];
}

println chan_names

//println "Markers "
//println list_markers

def downsample = 1
double xOrigin = 0
double yOrigin = 0
ImagePlane plane = ImagePlane.getDefaultPlane()

File directory = new File(dir_project)
if (!directory.exists())
{
	println("No project directory, creating one!")
	directory.mkdirs()
}

// Create project
def project = Projects.createProject(directory , BufferedImage.class)

// Build a list of files
def files = []
selectedDir = new File(dir_ome)
selectedDir.eachFileRecurse (FileType.FILES) { file ->
	if ((file.getName().toLowerCase().endsWith(".ome.tif")) || (file.getName().toLowerCase().endsWith(".ome.tiff")))
	{
		if(file.getName().contains(regionSet)){
			files << file
		}
	}
}

print(files)


println('---')
// Add files to the project
for (file in files) {
	def imagePath = file.getCanonicalPath()
	println(imagePath)
	
	// Get serverBuilder
	def support = ImageServerProvider.getPreferredUriImageSupport(BufferedImage.class, imagePath)
	println(support)
	def builder = support.builders.get(0)

	// Make sure we don't have null 
	if (builder == null) {
		print "Image not supported: " + imagePath
		continue
	}
	
	// Add the image as entry to the project
	print "Adding: " + imagePath
	entry = project.addImage(builder)
	
	// Set a particular image type
	def imageData = entry.readImageData()
	imageData.setImageType(ImageData.ImageType.FLUORESCENCE)
	
	// set channel names from csv file
	setChannelNames(imageData, chan_names)
	
	print("Clearing objects from image")
	imageData.getHierarchy().clearAll()
	
	entry.saveImageData(imageData)

	// Write a thumbnail if we can
	var img = ProjectCommands.getThumbnailRGB(imageData.getServer());
	entry.setThumbnail(img)

	// Add an entry name (the filename)
	entry.setImageName(file.getName())

	
}


// Changes should now be reflected in the project directory
project.syncChanges()


File directoryOfMasks = new File(dir_masks)
if (directoryOfMasks.exists()){
	println("Discovering Mask Files...")
	def wholecellfiles = []
	directoryOfMasks.eachFileRecurse (FileType.FILES) { file ->
	if (file.getName().endsWith("cell.tif"))//# "_WholeCellMask.tiff"
		{ wholecellfiles << file }
	}
	print "list of masks" + wholecellfiles
	
	for (entry in project.getImageList()) {
		imgName = entry.getImageName()
		print imgName
		String sample = imgName[imgName.lastIndexOf(':')+1..-1].tokenize(".")[0]
		println(" >>> "+sample)
		def imageData = entry.readImageData()
		def server = imageData.getServer()
	
		//Mask File for Nuclei
		def nMask1 = wholecellfiles.find { it.toString().contains(sample) } // getName()
		if(nMask1 == null){
			println(" >>> MISSING MASK FILES!! <<<")
			println()
			continue
		}
				
		def imp = IJ.openImage(nMask1.absolutePath)
		int n = imp.getStatistics().max as int
		println("   Max Cell Label: "+n)
		if (n == 0) {
			print 'No objects found!'
			return
		}
		def ip = imp.getProcessor()
		if (ip instanceof ColorProcessor) {
			throw new IllegalArgumentException("RGB images are not supported!")
		}
		def roisIJ = RoiLabeling.labelsToConnectedROIs(ip, n)
		def rois = roisIJ.collect {
			if (it == null)
				return
			return IJTools.convertToROI(it, 0, 0, downsample, plane);
		}
		rois = rois.findAll{null != it}
		// Convert QuPath ROIs to objects
		def pathObjects = rois.collect {
			return PathObjects.createDetectionObject(it)
		}
		println("   Number of PathObjects: "+pathObjects.size() )
		imageData.getHierarchy().addObjects(pathObjects)
		resolveHierarchy()
		entry.saveImageData(imageData)
		
		println(" >>> Calculating measurements...")
                println(imageData.getHierarchy())
                println("  DetectionObjects:"+imageData.getHierarchy().getDetectionObjects().size())        
                def measurements = ObjectMeasurements.Measurements.values() as List
                println(measurements)
                for (detection in imageData.getHierarchy().getDetectionObjects()) {
                        ObjectMeasurements.addIntensityMeasurements( server, detection, downsample, measurements, [] )
                        ObjectMeasurements.addShapeMeasurements( detection, server.getPixelCalibration(), ObjectMeasurements.ShapeFeatures.values() )
                     
                        // ECG capture x and y coordinates in pixels 
                        double x = detection.getROI().getCentroidX()
        		double y = detection.getROI().getCentroidY()
        
                        detection.getMeasurementList().putMeasurement("centroid_px_x",x)
                        detection.getMeasurementList().putMeasurement("centroid_px_y",y)
                        
                        // ECG get mask value at pixel
                        id_label = ip.getValue(x.round(0).intValue(),y.round(0).intValue())
                        detection.getMeasurementList().putMeasurement("mask_label",id_label)  
                
         }
         fireHierarchyUpdate()
         entry.saveImageData(imageData)
         imageData.getServer().close() // best to do this...
	 }
}

project.syncChanges()

println("")
println("Done.")