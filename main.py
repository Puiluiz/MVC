from controller import CowStrikeController
from model import CowStrikeModel
from view import CowStrikeView


if __name__ == "__main__":
    model = CowStrikeModel()
    view = CowStrikeView()
    controller = CowStrikeController(model, view)
    controller.run()