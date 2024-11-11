from PIL import Image
import torch
from torchvision import transforms
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
import base64
from io import BytesIO

class Image_Augmentation:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(self.image_path).convert('RGB')
        self.image_tensor = transforms.ToTensor()(self.image)

    def image_to_base64(self, image):
        """Convert PIL Image or tensor to base64 string"""
        if isinstance(image, torch.Tensor):
            # Convert tensor to PIL Image
            if image.dim() == 3:
                image = transforms.ToPILImage()(image)
            else:
                image = transforms.ToPILImage()(image.squeeze())
        elif not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL Image or torch Tensor")

        # Convert PIL Image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    def resize_image(self, size=(256, 256)):
        """Resize the image"""
        resize_transform = transforms.Resize(size)
        resized_image = resize_transform(self.image)
        return resized_image

    def convert_to_grayscale(self):
        """Convert image to grayscale"""
        grayscale_transform = transforms.Grayscale(num_output_channels=3)
        return grayscale_transform(self.image)

    def normalize_img(self):
        """Normalize the image"""
        tensor_image = transforms.ToTensor()(self.image)
        mean = tensor_image.mean()
        std = tensor_image.std()
        normalize_transform = transforms.Normalize(mean=[mean.item()]*3, std=[std.item()]*3)
        normalized_tensor = normalize_transform(tensor_image)
        return transforms.ToPILImage()(normalized_tensor)

    def random_crop(self, size=(224, 224)):
        """Randomly crop the image"""
        crop_transform = transforms.RandomCrop(size)
        return crop_transform(self.image)

    def random_horizontal_flip(self, p=0.5):
        """Randomly flip the image horizontally"""
        if torch.rand(1) < p:
            return transforms.functional.hflip(self.image)
        return self.image

    def random_rotation(self, degrees=30):
        """Randomly rotate the image"""
        angle = torch.randint(-degrees, degrees + 1, (1,)).item()
        return transforms.functional.rotate(self.image, angle)

    def color_jitter(self, brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1):
        """Apply color jitter to the image"""
        jitter_transform = transforms.ColorJitter(
            brightness=brightness,
            contrast=contrast,
            saturation=saturation,
            hue=hue
        )
        return jitter_transform(self.image)

    def add_gaussian_noise(self, mean=0., std=0.1):
        """Add Gaussian noise to the image"""
        tensor_image = transforms.ToTensor()(self.image)
        noise = torch.randn_like(tensor_image) * std + mean
        noisy_image = torch.clamp(tensor_image + noise, 0, 1)
        return transforms.ToPILImage()(noisy_image)

    def random_erasing(self, p=0.5, scale=(0.02, 0.33), ratio=(0.3, 3.3)):
        """Randomly erase a rectangular region from the image"""
        tensor_image = transforms.ToTensor()(self.image)
        erasing_transform = transforms.RandomErasing(
            p=p,
            scale=scale,
            ratio=ratio,
            value='random'
        )
        erased_tensor = erasing_transform(tensor_image)
        return transforms.ToPILImage()(erased_tensor)

    def elastic_transform(self, alpha=50, sigma=5):
        """
        Apply elastic deformation to the image.
        
        Parameters:
        - alpha: Scaling factor for deformation
        - sigma: Smoothing factor for deformation
        """
        try:
            # Convert image to numpy array
            tensor_image = transforms.ToTensor()(self.image)
            image_numpy = tensor_image.numpy().transpose(1, 2, 0)
            
            # Generate random displacement fields
            shape = image_numpy.shape[:2]
            dx = gaussian_filter((np.random.rand(*shape) * 2 - 1), sigma) * alpha
            dy = gaussian_filter((np.random.rand(*shape) * 2 - 1), sigma) * alpha
            
            # Generate mesh grid
            x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
            
            # Create distorted indices
            indices = [
                np.reshape(y + dy, (-1, 1)),
                np.reshape(x + dx, (-1, 1))
            ]
            
            # Apply transformation to each channel
            distorted_image = np.zeros_like(image_numpy)
            for c in range(image_numpy.shape[2]):
                distorted_image[:, :, c] = map_coordinates(
                    image_numpy[:, :, c],
                    indices,
                    order=1,
                    mode='reflect'
                ).reshape(shape)
            
            # Ensure values are in valid range
            distorted_image = np.clip(distorted_image, 0, 1)
            
            # Convert back to PIL Image
            tensor_result = torch.from_numpy(distorted_image.transpose(2, 0, 1))
            return transforms.ToPILImage()(tensor_result)
            
        except Exception as e:
            print(f"Error in elastic transform: {str(e)}")
            # Return original image if transformation fails
            return self.image

    def histogram_equalization(self):
        """Apply histogram equalization to the image"""
        return transforms.functional.equalize(self.image)

    def adjust_brightness(self, brightness_factor=1.5):
        """Adjust the brightness of the image"""
        return transforms.functional.adjust_brightness(self.image, brightness_factor)

    def adjust_contrast(self, contrast_factor=1.5):
        """Adjust the contrast of the image"""
        return transforms.functional.adjust_contrast(self.image, contrast_factor)

    def adjust_saturation(self, saturation_factor=1.5):
        """Adjust the saturation of the image"""
        return transforms.functional.adjust_saturation(self.image, saturation_factor)

    def center_crop(self, size=(224, 224)):
        """Crop the center of the image"""
        center_crop_transform = transforms.CenterCrop(size)
        return center_crop_transform(self.image)

    def gaussian_blur(self, kernel_size=11, sigma=2.0):
        """Apply Gaussian blur to the image"""
        blur_transform = transforms.GaussianBlur(kernel_size, sigma)
        return blur_transform(self.image)

    def solarize(self, threshold=128):
        """Apply solarization to the image"""
        return transforms.functional.solarize(self.image, threshold)

    def posterize(self, bits=2):
        """Apply posterization to the image"""
        return transforms.functional.posterize(self.image, bits)

    def adjust_sharpness(self, sharpness_factor=2.0):
        """Adjust the sharpness of the image"""
        return transforms.functional.adjust_sharpness(self.image, sharpness_factor)
