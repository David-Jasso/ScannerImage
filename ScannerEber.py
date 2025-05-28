import cv2 as cv
import numpy as np

#Funcion para realizar eventos del Mouse.
def onMouseEvent(event, x, y, flags, userData):
    #Variables globales del programa
    #print(event, x, y).
    global src_points
    global img
    global dst_points
    global dst_img
    global scan_count

    if event == cv.EVENT_LBUTTONUP:
        #Aplicar los puntos en sentido horario.
        src_points.append((x,y))
        cv.circle(img, (x,y), 2, (255, 0, 0), -1)
        cv.imshow("Buscando Documento", img)
        print(event, x, y)
 
        if len(src_points) == 4:
            #Aplicar homografia y transformación de perpectiva.
            h, status = cv.findHomography(np.array(src_points), np.array(dst_points))
            dst_img = cv.warpPerspective(img, h, (dst_img.shape[1], dst_img.shape[0]))

            #Mostrar resultado y guardar imagen en formato PDF.
            filename = f"6-ProcesamientoAvanzado/data/Scan_{scan_count}.png"
            cv.imshow("Scanner Finalizado", dst_img)
            cv.imwrite(filename, dst_img)
            scan_count += 1

def main():
    #Variables globales del programa
    global src_points
    global dst_points
    global dst_img
    global img
    global scan_count

    #Inicio del contador de imagenes
    scan_count = 0

    #Puntos de imagen fuente y puntos de imagen destino.
    src_points = []                                     
    dst_points = [(0,0), (350,0), (350,500), (0,500)] 

    #Crear imagen destino de 500 x 350 pixeles.
    dst_img = np.zeros((500, 350), dtype = np.uint8)

    #Crear Objeto Video Capture para leer un video.
    cap = cv.VideoCapture(0)
    frame = None

    #LLamar Buscando Documento a la captura de video.
    cv.namedWindow('Buscando Documento')

    #Llamar funcion de eventos del mouse en la captura de video.
    cv.setMouseCallback("Buscando Documento", onMouseEvent)
 
    #Comprobar si la cámara se ha abierto correctamente.
    if not cap.isOpened():
        print("Error al conectar con la camara para Scanner de Documentos... ")
        exit()
    
    while True:
        #Leer captura de video.
        ret, frame = cap.read()
        img = frame.copy()

        #Mostrar ventana Buscando Documento.
        cv.imshow('Buscando Documento', img)

        #Tiempo de espera de 25ms entre cada frame.
        key = cv.waitKey(25)

        if key == ord('q'): ##convierte letra a valor ASCI.
            break
        elif key == ord('r'):
            src_points = []
            cv.destroyWindow("Scanner Finalizado")

    #Liberar los objetos VideoCapture y destruye todas las ventanas creadas.
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main() 