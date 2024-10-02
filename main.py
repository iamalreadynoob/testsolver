import visual
import functionality

if __name__ == '__main__':
    model, gemini = functionality.starter()

    screen = visual.launch(model, gemini)
    screen.mainloop()