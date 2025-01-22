import pygame as p
from index import chessEngine

p.init()
p.display.set_caption("Chess")

WIDTH = HEIGHT = 800

screen = p.display.set_mode([WIDTH, HEIGHT])
clock = p.time.Clock()
sprites = p.sprite.Group()


class GUI():
    images = {}

    def __init__(self, board):

        self.surface = self.createBoardsurf()
        self._loadImages()
        self._refreshBoard(board)

    def _loadImages(self):
        pieces = ["wp", "wk", "wr", "wq", "wh",
                  "wb", "bb", "bk", "bq", "br", "bp", "bh"]
        for piece in pieces:
            self.images[piece] = p.transform.scale(p.image.load(
                f"views\\Chess_Pieces\\{piece}.png"), (80, 80))

    def _refreshBoard(self, board):
        for r in range(0, 8):
            for c in range(0, 8):

                if (board[r][c] != "--"):
                    self.surface[r][c]._updateImg(self.images[board[r][c]])
                else:
                    self.surface[r][c]._updateImg("")
                self.surface[r][c].selected = False

    def createBoardsurf(self):

        board_surf = []
        COLORS = [[(238, 238, 210), (250, 250, 250)],
                  [(118, 150, 86), (0, 160, 90)]]

        for y in range(0, HEIGHT, 100):
            row = []

            for x in range(0, WIDTH, 100):

                color = COLORS[(int((x/100)+(y/100)) % 2)]
                board = tile(x, y, color[0], color[1],
                             p.Rect(x, y, 100, 100))

                sprites.add(board)
                row.append(board)

            board_surf.append(row)

        return board_surf


class tile(p.sprite.Sprite):
    def __init__(self, x, y, color, color_hover, rect):

        super().__init__()

        self.x = x
        self.y = y

        self.color = color
        self.color_hover = color_hover
        self.selected = False

        self.tmp_rect = p.Rect(0, 0, 100, 100)

        self.org = self._createSurf(
            color, self.tmp_rect)
        self.hov = self._createSurf(
            color_hover, self.tmp_rect)

        self.image = self.org
        self.rect = rect

    def _updateImg(self, pieceImg):
        self.org = self._createSurf(
            self.color, self.tmp_rect)
        self.hov = self._createSurf(
            self.color_hover, self.tmp_rect)
        if pieceImg != "":
            tile_content = pieceImg.get_rect(center=self.tmp_rect.center)
            self.org.blit(pieceImg, tile_content)
            self.hov.blit(pieceImg, tile_content)

    def _createSurf(self, color, rect):
        img = p.Surface(rect.size)
        img.fill(color)

        return img

    def update(self, events, engine, Gui):
        pos = p.mouse.get_pos()

        hit = self.rect.collidepoint(pos)
        self.image = self.hov if hit or self.selected else self.org

        for event in events:

            if event.type == p.MOUSEBUTTONDOWN and hit:
                coords = [int(self.y/100), int(self.x/100)]
                self.selected = True

                engine._processClick(coords, Gui)
                for i in engine.validMoves:
                    if i.startRow == coords[0] and i.startColumn == coords[1]:
                        Gui.surface[i.endRow][i.endColumn].selected = True
                if engine.storedPiece == []:
                    Gui._refreshBoard(chess_Engine.board)


if __name__ == '__main__':

    running = True
    chess_Engine = chessEngine()
    gui = GUI(chess_Engine.board)

    while running:
        p.mouse.set_cursor(p.cursors.Cursor(p.SYSTEM_CURSOR_HAND))

        events = p.event.get()

        for event in events:
            if event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    chess_Engine.Z_keyPress()
                    gui._refreshBoard(chess_Engine.board)
            if event.type == p.QUIT:
                running = False

        sprites.update(events, chess_Engine, gui)   # <-- Check for any events
        screen.fill(p.Color('white'))
        sprites.draw(screen)
        clock.tick(30)

        p.display.flip()

    p.quit()
