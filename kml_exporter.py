def export_navpoints_to_kml(filename, navpoints):
    with open(filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('  <Document>\n')
        f.write('    <name>Puntos de Navegaci\u00f3n</name>\n')

        for p in navpoints:
            f.write('    <Placemark>\n')
            f.write(f'      <name>{p.name}</name>\n')
            f.write('      <Point>\n')
            f.write(f'        <coordinates>{p.longitude},{p.latitude}</coordinates>\n')
            f.write('      </Point>\n')
            f.write('    </Placemark>\n')

        f.write('  </Document>\n')
        f.write('</kml>\n')

def export_segments_to_kml(filename, segments, navpoints_by_number):
    with open(filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('  <Document>\n')
        f.write('    <name>Segmentos</name>\n')

        for s in segments:
            p1 = navpoints_by_number[s.origin_number]
            p2 = navpoints_by_number[s.destination_number]
            f.write('    <Placemark>\n')
            f.write(f'      <name>{p1.name} - {p2.name}</name>\n')
            f.write('      <LineString>\n')
            f.write('        <coordinates>\n')
            f.write(f'          {p1.longitude},{p1.latitude}\n')
            f.write(f'          {p2.longitude},{p2.latitude}\n')
            f.write('        </coordinates>\n')
            f.write('      </LineString>\n')
            f.write('    </Placemark>\n')

        f.write('  </Document>\n')
        f.write('</kml>\n')

def export_path_to_kml(filename, path_nodes):
    with open(filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('  <Document>\n')
        f.write('    <name>Camino m\u00e1s corto</name>\n')

        f.write('    <Placemark>\n')
        f.write('      <name>Ruta</name>\n')
        f.write('      <LineString>\n')
        f.write('        <coordinates>\n')
        for p in path_nodes:
            f.write(f'          {p.longitude},{p.latitude}\n')
        f.write('        </coordinates>\n')
        f.write('      </LineString>\n')
        f.write('    </Placemark>\n')

        f.write('  </Document>\n')
        f.write('</kml>\n')
