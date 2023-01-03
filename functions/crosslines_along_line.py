


def crosslines_along_line (line_layer_dir, crosslines_dir, interval_distance, cross_length, degree):
    line_layer=QgsVectorLayer(line_layer_dir,"line_layer", "ogr")
    line_features = line_layer.getFeatures()
    
    linecrs=line_layer.crs().authid()
    uri = "LineString?crs="+linecrs
    crosslines_layer=QgsVectorLayer(uri, "layer", "memory")

    expression1 = QgsExpression('$length')
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(line_layer))
    
    
    for line_f in line_features:
        
        context.setFeature(line_f)
        length=expression1.evaluate(context)
        
        counter=int(length/interval_distance)
        interp_distance=0
        for j in range(0,counter+1):
            
           
            point_0 = line_f.geometry().interpolate(interp_distance)
            point_1 = line_f.geometry().interpolate(interp_distance+0.001)
            
            point_0_x=point_0.asPoint().x()
            point_0_y=point_0.asPoint().y()
            
            point_1_x=point_1.asPoint().x()
            point_1_y=point_1.asPoint().y()
            

            rotated_point_1_x=math.cos((degree/360)*2*math.pi)*(point_1_x-point_0_x)-math.sin((degree/360)*2*math.pi)*(point_1_y-point_0_y)+point_0_x
            rotated_point_1_y=math.cos((degree/360)*2*math.pi)*(point_1_y-point_0_y)+math.sin((degree/360)*2*math.pi)*(point_1_x-point_0_x)+point_0_y
            
            if (rotated_point_1_x-point_0_x)!=0:
               
                slope=(rotated_point_1_y-point_0_y)/(rotated_point_1_x-point_0_x)
            
                new_point_1_x=point_0_x+(cross_length**2/(1+slope**2))**(0.5)
                new_point_1_y=point_0_y+slope*(new_point_1_x-point_0_x)
            
                new_point_2_x=point_0_x-(cross_length**2/(1+slope**2))**(0.5)
                new_point_2_y=point_0_y+slope*(new_point_2_x-point_0_x)
            else:
                new_point_1_x=point_0_x
                new_point_1_y=point_0_y+cross_length
                    
                new_point_2_x=point_0_x
                new_point_2_y=point_0_y-cross_length
                    
            new_point_1=QgsPoint(new_point_1_x,new_point_1_y)
            new_point_2=QgsPoint(new_point_2_x,new_point_2_y)
            new_line=QgsGeometry.fromPolyline([new_point_1,new_point_2])
            
            new_line_feature = QgsFeature()
            new_line_feature.setGeometry(new_line)
            crosslines_layer.dataProvider().addFeature(new_line_feature)

            interp_distance=interp_distance+(interval_distance)
            

    writer = QgsVectorFileWriter.writeAsVectorFormat(crosslines_layer,crosslines_dir, 'UTF-8', crosslines_layer.crs(), 'ESRI Shapefile')
    del(writer)
    
    
    
    
    
    


