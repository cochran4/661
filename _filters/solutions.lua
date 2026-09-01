function Pandoc(doc)
  local value = doc.meta["show-solutions"]
  local show_solutions = value ~= nil and pandoc.utils.stringify(value):lower() == "true"

  doc.blocks = doc.blocks:walk({
    Div = function(div)
      if not div.classes:includes("answer-block") then
        return nil
      end

      if not show_solutions then
        return {}
      end

      local blocks = pandoc.List:new()
      blocks:insert(pandoc.RawBlock("html", '<details class="solution"><summary>Reveal solution</summary><div class="solution-body">'))
      blocks:extend(div.content)
      blocks:insert(pandoc.RawBlock("html", "</div></details>"))
      return blocks
    end
  })

  return doc
end
