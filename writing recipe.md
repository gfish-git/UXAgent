Here’s a cleaner and more streamlined rewrite of your file:

---

# Writing a Recipe for Web Element Processing

A **recipe** is used to recursively filter website elements based on selectors and pass them to the agent. It defines how to extract information, identify clickable elements, and generate an abstract representation of a web page. Each matching DOM element is transformed into a new abstract element according to the recipe.

---

## Recipe Selection: Identifying the Target Page

| **Field Name** | **Type** | **Description**                                                                |
|----------------|----------|--------------------------------------------------------------------------------|
| `match`        | `string` | Root-level identifier for matching specific page features.                     |
| `match_method` | `string` | Specifies how to match (`"text"` or `"url"`). Defaults to `"text"` if omitted. |

- **"text" Method:** Uses a CSS selector to find elements defined by the `match` attribute.
- **"url" Method:** Checks if the `match` string appears in the current URL.

---

## Creating Abstract Elements

| **Field Name** | **Type**       | **Description**                                                           |
|----------------|----------------|---------------------------------------------------------------------------|
| `selector`     | `CSS selector` | Identifies elements in the DOM to include in the abstract representation. |

---

## Extracting Text Content

| **Field Name**  | **Type**       | **Description**                                           |
|-----------------|----------------|-----------------------------------------------------------|
| `text_selector` | `CSS selector` | Selects child elements for extracting text.               |
| `add_text`      | `bool`         | Determines whether to include the element's text content. |
| `text_js`       | `JavaScript`   | Executes code to process and extract text.                |
| `text_format`   | `string`       | Specifies text formatting using `{}` placeholders.        |

- If `text_selector` is specified, text is extracted from the matching child elements.
- If `text_js` is provided, it is executed to process the text.
- If `add_text` is `true`, the element's text content is used.
- `text_format` applies custom formatting to the extracted text.

---

## Generating Element Names

| **Field Name** | **Type** | **Description**                                                                  |
|----------------|----------|----------------------------------------------------------------------------------|
| `name`         | `string` | Defines naming rules for elements, ensuring each child includes its parent path. |

- `name` as a string directly sets the element name.
- `"from_text"` generates the name from the element's text content.
- `"from_nth_child"` uses the ordinal position of the child element.

---

## Marking Clickable Elements and Inputs

| **Field Name**   | **Type**       | **Description**                                                           |
|------------------|----------------|---------------------------------------------------------------------------|
| `clickable`      | `bool`         | Marks an element as clickable and adds metadata for interactivity.        |
| `click_selector` | `CSS selector` | Locates the actual clickable child element, if different from the parent. |

- **For Clickable Elements:**
  - `name` must be defined.
  - If `click_selector` is provided, it locates the clickable child; otherwise, the parent is used.
  - Adds a `data-clickable-id` attribute for event binding.
  
- **For Input Elements:**
  - Handles types like `text`, `number`, `checkbox`, and `radio`.
  - Stores input data in a global object.

---

## Processing `<select>` Elements

- Adds a `data-select-id` attribute to the `<select>` element.
- Iterates through child `<option>` elements to:
  - Extract `value` and `text`.
  - Create new abstract `<option>` elements with attributes like `value`, `name`, and `selected`.
  - Add a `data-clickable-id` to bind selection actions.

---

## Copying and Overwriting Attributes

| **Field Name**  | **Type** | **Description**                                                                           |
|-----------------|----------|-------------------------------------------------------------------------------------------|
| `keep_attr`     | `list`   | Specifies attributes to copy to the new element.                                          |
| `override_attr` | `object` | Attributes to override or add, with values calculated dynamically (e.g., via JavaScript). |
| `class`         | `string` | Assigns a CSS class to the new element.                                                   |

- By default, common attributes (`alt`, `title`, `type`, `value`) are copied.
- Use `keep_attr` to specify additional attributes.
- `class` and `id` can be explicitly set.
- `override_attr` supports dynamic values via JavaScript.

---

## Processing Child Elements

| **Field Name**              | **Type** | **Description**                                                               |
|-----------------------------|----------|-------------------------------------------------------------------------------|
| `children`                  | `array`  | Defines child elements like search boxes and buttons.                         |
| `insert_split_marker`       | `bool`   | Inserts markers for parallel processing in long lists (e.g., search results). |
| `insert_split_marker_every` | `number` | Sets the interval for adding split markers.                                   |
| `empty_message`             | `string` | Message to display when the parent element has no children.                   |
| `direct_child`              | `bool`   | Restricts selectors to match only direct children of the parent.              |

- If `children` is not specified, all child elements are removed, leaving only the parent.
- If defined:
  - Processes each child element recursively using `processElement`.
  - Inserts `<split-marker>` elements between child elements, if applicable.

---

## Example
Refer to the [amazon_recipes.py](./src/simulated_web_agent/executor/amazon_recipes.py) file for implementation details.

--- 

This version is more concise while retaining all essential details. Let me know if you'd like further tweaks!