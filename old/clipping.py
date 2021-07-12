
def pointClipping(point, border):
    if point.locX < border["xmin"] or point.locX > border["xmax"] or point.locY < border["ymin"] or point.locY > border["ymax"]:
        return None
    else:
        return point

def lineClippingCohenSutherland(line, border):

    coords1 = getCohenSutherlandCoords(line.p1, border)
    coords2 = getCohenSutherlandCoords(line.p2, border)
    if coords1 == 0 and coords2 == 0:
        return line # Totalmente contido
    if coords1 & coords2 != 0:
        return None  # Totalmente fora
    if coords1 != coords2 and coords1 & coords2 == 0:
        M = (line.p2.locY - line.p1.locY)/(line.p2.locX - line.p1.locX)
        if coords1 != 0:
            if not calculatePoint(M, coords1, line.p1, border):
                return None
        if coords2 != 0:
            if not calculatePoint(M, coords2, line.p2, border):
                return None
    return line

def calculatePoint(M, coords, point, border):
    xintersec = point.locX
    yintersec = point.locY
    if coords & (1<<1) > 0:
        yintersec = M * (border["xmax"] - point.locX) + point.locY
        xintersec = border["xmax"]
    elif coords & (1<<0) > 0:
        yintersec = M * (border["xmin"] - point.locX) + point.locY
        xintersec = border["xmin"]
    if yintersec >= border["ymin"] and yintersec <= border["ymax"]:
        point.locY = yintersec
        point.locX = xintersec
        return True
    if coords & (1<<3) > 0: 
        xintersec = (border["ymax"] - point.locY) / M + point.locX
        yintersec = border["ymax"]
    elif coords & (1<<2) > 0:
        xintersec = (border["ymin"] - point.locY) / M  + point.locX
        yintersec = border["ymin"]
    if xintersec >= border["xmin"] and xintersec <= border["xmax"]:
        point.locY = yintersec
        point.locX = xintersec
        return True
    if xintersec < border["xmin"] or xintersec > border["xmax"] or yintersec < border["ymin"] or yintersec > border["ymax"]:
        return False

def getCohenSutherlandCoords(point, border):
    bits = 0
    if point.locY >= border["ymax"]:
        bits |= (1<<3) # Cima
    elif point.locY <= border["ymin"]:
        bits |= (1<<2) # Baixo
    if point.locX >= border["xmax"]:
        bits |= (1<<1) # Direita
    elif point.locX <= border["xmin"]:
        bits |= (1<<0) # Esquerda
    return bits
    