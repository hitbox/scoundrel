from collections import defaultdict

class FrameAnimation:
    """
    Animation of frame images.
    """

    def __init__(self, frames, frame_duration):
        self.frames = frames
        self.frame_duration = frame_duration
        self.time = 0
        self.index = 0

    def update(self, elapsed):
        self.time += elapsed
        if self.time > self.frame_duration:
            self.time = 0
            self.index = (self.index + 1) % len(self.frames)

    def update_target(self, target):
        target.image = self.frames[self.index]


class AnimationManager:

    def __init__(self):
        self.animations = []
        self.unique_animations = set()
        self.sprite_for_animation = defaultdict(list)
        self.animation_for_sprite = {}

    def update(self, elapsed):
        # Update animation objects once and sprite targets' images.
        seen = set()
        for sprite, animation in self.animations:
            if animation not in seen:
                seen.add(animation)
                animation.update(elapsed)
            animation.update_target(sprite)

    def add(self, sprite, animation):
        self.animations.append((sprite, animation))
        self.unique_animations.add(animation)
        self.sprite_for_animation[animation].append(sprite)
        self.animation_for_sprite[sprite] = animation

    def get_sprites_for_animation(self, animation):
        for sprite, other in self.animations:
            if other is animation:
                yield sprite


def get_named_animations(assets, frame_duration=200):
    images = assets['new_platformer_pack']
    animations = {
        'pincer.pincing': FrameAnimation(
            frames = [
                images['pincer.open'],
                images['pincer.close'],
            ],
            frame_duration = frame_duration,
        ),
        'yellow_worm.wiggle': FrameAnimation(
            frames = [
                images['yellow_worm.wiggle1'],
                images['yellow_worm.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'blue_worm.wiggle': FrameAnimation(
            frames = [
                images['blue_worm.wiggle1'],
                images['blue_worm.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'snail.wiggle': FrameAnimation(
            frames = [
                images['snail.wiggle1'],
                images['snail.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'spikey_blob.wiggle': FrameAnimation(
            frames = [
                images['spikey_blob.wiggle1'],
                images['spikey_blob.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'purple_blob.wiggle': FrameAnimation(
            frames = [
                images['purple_blob.wiggle1'],
                images['purple_blob.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'fire_blob.wiggle': FrameAnimation(
            frames = [
                images['fire_blob.wiggle1'],
                images['fire_blob.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'green_block.squash_stretch': FrameAnimation(
            frames = [
                images['green_block.stretch1'],
                images['green_block.stretch2'],
            ],
            frame_duration = frame_duration,
        ),
        'bee.wiggle': FrameAnimation(
            frames = [
                images['bee.wiggle1'],
                images['bee.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'spike_flower.wiggle': FrameAnimation(
            frames = [
                images['spike_flower.wiggle1'],
                images['spike_flower.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'mouse.wiggle': FrameAnimation(
            frames = [
                images['mouse.wiggle1'],
                images['mouse.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'black_snail.wiggle': FrameAnimation(
            frames = [
                images['black_snail.wiggle1'],
                images['black_snail.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'fly.wiggle': FrameAnimation(
            frames = [
                images['fly.wiggle1'],
                images['fly.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'yellow_fish.wiggle': FrameAnimation(
            frames = [
                images['yellow_fish.wiggle1'],
                images['yellow_fish.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
        'purple_fish.wiggle': FrameAnimation(
            frames = [
                images['purple_fish.up'],
                images['purple_fish.down'],
            ],
            frame_duration = frame_duration,
        ),
        'blue_fish.wiggle': FrameAnimation(
            frames = [
                images['blue_fish.wiggle1'],
                images['blue_fish.wiggle2'],
            ],
            frame_duration = frame_duration,
        ),
    }
    return animations
