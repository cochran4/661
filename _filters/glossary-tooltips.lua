local definitions = {}

local function normalize(text)
  return text:lower():gsub("[^%w]+", "-"):gsub("^-", ""):gsub("-$", "")
end

local function load_definitions()
  local file = io.open("glossary.qmd", "r")
  if not file then
    io.stderr:write("Could not open glossary.qmd while creating glossary tooltips.\n")
    return
  end

  local term = nil
  for line in file:lines() do
    local heading = line:match("^%*%*(.-)%*%*%s*$")
    if heading then
      term = normalize(heading)
    elseif term and line:match("%S") and not line:match("^%-%-%-$") then
      definitions[term] = line
      term = nil
    end
  end
  file:close()
end

load_definitions()

function Span(span)
  if not span.classes:includes("glossary-term") then
    return nil
  end

  local label = pandoc.utils.stringify(span.content)
  local requested_term = span.attributes["data-glossary"] or label
  local definition = definitions[normalize(requested_term)]

  if not definition then
    io.stderr:write("No glossary definition found for '" .. requested_term .. "'.\n")
    return nil
  end

  span.attributes["data-glossary"] = nil
  span.attributes["data-bs-toggle"] = "tooltip"
  span.attributes["data-bs-title"] = definition
  span.attributes["tabindex"] = "0"
  return span
end
