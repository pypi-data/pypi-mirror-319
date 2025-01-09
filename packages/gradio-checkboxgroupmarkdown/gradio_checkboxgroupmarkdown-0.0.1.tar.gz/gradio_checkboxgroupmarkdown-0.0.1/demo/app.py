
import gradio as gr


from typing import List
import gradio as gr
from dataclasses import dataclass
import random
from gradio_checkboxgroupmarkdown import CheckboxGroupMarkdown

# Define two different sets of choices
ai_choices = [
    {
        "id": "art_101",
        "title": "Understanding Neural Networks",
        "content": "# Understanding Neural Networks\nThis article explains the basics of neural networks, their architecture, and how they learn from data."
    },
    {
        "id": "art_102", 
        "title": "A Gentle Introduction to Transformers",
        "content": "# A Gentle Introduction to Transformers\nTransformers have revolutionized NLP. Learn about attention mechanisms, encoder-decoder architecture, and more."
    },
    {
        "id": "art_103",
        "title": "Reinforcement Learning Basics",
        "content": "# Reinforcement Learning Basics\nAn overview of RL concepts like agents, environments, rewards, and policies."
    }
]

ml_choices = [
    {
        "id": "art_104",
        "title": "Machine Learning Fundamentals",
        "content": "# Machine Learning Fundamentals\nLearn about supervised, unsupervised, and reinforcement learning approaches."
    },
    {
        "id": "art_105",
        "title": "Deep Learning vs Traditional ML",
        "content": "# Deep Learning vs Traditional ML\nUnderstand the key differences between deep learning and traditional machine learning."
    },
    {
        "id": "art_106",
        "title": "Feature Engineering",
        "content": "# Feature Engineering\nMaster the art of creating meaningful features from raw data."
    }
]

def sentence_builder(selected):
    if not selected:
        return "You haven't selected any articles yet."
    
    if isinstance(selected[0], dict) and "title" in selected[0]:
        formatted_choices = []
        for choice in selected:
            formatted_choices.append(
                f"ID: {choice['id']}\nTitle: {choice['title']}\nContent: {choice['content']}"
            )
        return "Selected articles are:\n\n" + "\n\n".join(formatted_choices)
    else:
        return "Selected articles are:\n\n- " + "\n- ".join(selected)

def update_choices(choice_type: str):
    if choice_type == "AI":
        return gr.update(choices=ai_choices, value=[]), ""
    elif choice_type == "ML":
        return gr.update(choices=ml_choices, value=["art_106"]), ""
    else:  # Random mix
        mixed_choices = random.sample(ai_choices + ml_choices, 3)
        return gr.update(choices=mixed_choices, value=[]), ""


with gr.Blocks() as demo:
    gr.Markdown("## Interactive Article Selection Demo")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Change Article Categories")
            with gr.Row():
                ai_btn = gr.Button("AI Articles", variant="primary")
                ml_btn = gr.Button("ML Articles", variant="secondary")
                mix_btn = gr.Button("Random Mix", variant="secondary")
    
    with gr.Row():
        with gr.Column(scale=2):
            checkbox_group = CheckboxGroupMarkdown(
                choices=ai_choices,  # Start with AI choices
                label="Select Articles",
                info="Choose articles to include in your collection",
                type="title"
            )
        
        with gr.Column(scale=1):
            output_text = gr.Textbox(
                label="Selected Articles",
                placeholder="Make selections to see results...",
                info="Selected articles will be displayed here",
                lines=10
            )
    
    # Event handlers
    checkbox_group.change(
        fn=sentence_builder,
        inputs=checkbox_group,
        outputs=output_text
    )
    
    # Button click handlers to update choices
    ai_btn.click(
        fn=lambda: update_choices("AI"),
        inputs=None,
        outputs=[checkbox_group, output_text],
    )

    ml_btn.click(
        fn=lambda: update_choices("ML"),
        inputs=None, 
        outputs=[checkbox_group, output_text],
    )

    mix_btn.click(
        fn=lambda: update_choices("MIX"),
        inputs=None,
        outputs=[checkbox_group, output_text],
    )

if __name__ == '__main__':
    demo.launch()