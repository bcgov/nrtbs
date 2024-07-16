import matplotlib.pyplot as plt
import matplotlib.patches as patches
from plot import plot_image
# from misc import args
import sys
args = sys.argv

def plot_image_with_rectangle(file):
    """
    Plots an image and allows the user to draw a rectangle on the image.
    Displays the rectangle's position and dimensions.
    Takes a bin file name
    """

    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Display the image
    image = plot_image(file)
    print(image)
    ax.imshow(image) # plot initial image
    # Initialize variables to store the rectangle's position
    rect = None
    start_x = start_y = 0
    is_drawing = False

    def on_mouse_press(event):
        nonlocal start_x, start_y, is_drawing
        if event.inaxes != ax:
            return
        start_x = event.xdata
        start_y = event.ydata
        is_drawing = True
        print(f"Start Drawing at: ({start_x:.2f}, {start_y:.2f})")

    def on_mouse_drag(event):
        nonlocal rect, is_drawing
        if event.inaxes != ax or not is_drawing:
            return
        end_x = event.xdata
        end_y = event.ydata
        if rect is not None:
            rect.remove()
        width = end_x - start_x
        height = end_y - start_y
        rect = patches.Rectangle(
            (start_x, start_y), width, height,
            linewidth=1, edgecolor='r', facecolor='none'
        )
        ax.add_patch(rect)
        fig.canvas.draw_idle()
        print(f"Drawing rectangle: ({start_x:.2f}, {start_y:.2f}) to ({end_x:.2f}, {end_y:.2f})")

    def on_mouse_release(event):
        nonlocal is_drawing
        if event.inaxes != ax or not is_drawing:
            return
        end_x = event.xdata
        end_y = event.ydata
        width = end_x - start_x
        height = end_y - start_y
        print(f"Rectangle drawn from ({start_x:.2f}, {start_y:.2f}) to ({end_x:.2f}, {end_y:.2f})")
        print(f"Width: {width:.2f}, Height: {height:.2f}")
        is_drawing = False
        return [start_x, start_y, end_x, end_y]

    # Connect the event handlers
    fig.canvas.mpl_connect('button_press_event', on_mouse_press)
    fig.canvas.mpl_connect('motion_notify_event', on_mouse_drag)
    fig.canvas.mpl_connect('button_release_event', on_mouse_release)

    # Show the plot
    print('Show')
    plt.show()

# if __name__ == "__main__":
#     plot_image_with_rectangle(args[1])
